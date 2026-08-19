---
title: Mac 邮件连不上 Gmail：用 Xray 和 WARP 单独绕行
date: 2026-08-19 10:30:00
cover: /img/assets/Mac邮件连不上Gmail：用Xray和WARP单独绕行/cover.png
thumbnail: /img/assets/Mac邮件连不上Gmail：用Xray和WARP单独绕行/cover.png
categories:
- 折腾
tags:
- macOS
- Gmail
- Xray
- WARP
- VPS
toc: true
---

前段时间换了一台小流量 VPS，价格很合适，出口 IP 也不错。网页、终端和日常代理都很正常，偏偏 macOS 自带的邮件 App 里，Gmail 一直显示离线。

这种故障很容易让人先怀疑客户端：账号是不是过期了，Surge 规则有没有冲突，Xray 换协议时是不是改坏了配置。我折腾了一圈才发现，问题其实出在 VPS 到 Gmail 邮件服务器的直连路径上。后来我用 WireProxy 给 Xray 增加了一条 WARP 出口，只让 Gmail 的邮件端口绕行，其他流量继续使用原来的 VPS IP。

现在服务商已经恢复了这些端口，我也把特殊分流撤掉了。不过这套方法确实解决过问题，还是值得留一份能复现、也知道什么时候该删除的记录。

<!-- more -->

## 先把故障定位到服务器

Gmail 网页能打开，不代表邮件客户端使用的端口也能连接。Google 的说明里，IMAP 收信使用 `imap.gmail.com:993`，SMTP 发信通常使用 `smtp.gmail.com:587`，SSL 方式也可能使用 `465`。[Gmail 第三方邮件客户端设置](https://support.google.com/a/answer/9003945?hl=en-na)

我当时直接在 VPS 上测试：

```bash
timeout 8 nc -vz imap.gmail.com 993
timeout 8 nc -vz smtp.gmail.com 465
timeout 8 nc -vz smtp.gmail.com 587
```

结果是 SMTP 465 可以建立连接，IMAP 993 一直等到超时。这个结果基本排除了 Mac 邮件 App、客户端代理入口和 Gmail 账号本身：请求已经到了 VPS，接下来是 VPS 到 Gmail 的路径不通。

至于是不是服务商明确封了 993，单凭这个测试还不能下结论。也可能是上游路由或过滤策略出了问题。对使用者来说，能确定的是这条直连路径暂时不可用。

## 为什么不让整台服务器都走 WARP

这台 VPS 的出口 IP 本身是我想保留的。如果开启全局 WARP，Gmail 可能恢复，其他网站看到的出口却会一起变成 Cloudflare，等于为一个端口问题改掉整台机器的网络行为。

我需要的是一条很窄的旁路：

```text
macOS 邮件 App
       ↓
      Xray
       ├─ Gmail 的 465 / 587 / 993 → 本地 SOCKS → WireProxy / WARP
       └─ 其他流量              → VPS 原出口直连
```

[WireProxy](https://github.com/windtf/wireproxy) 是一个用户态 WireGuard 客户端，可以在本机暴露 SOCKS5 代理，不必创建接管全局流量的网络接口。WARP 这边负责提供另一条加密出口；Cloudflare 目前的客户端文档也说明，其隧道可使用 WireGuard 或 MASQUE。[Cloudflare One Client 说明](https://developers.cloudflare.com/cloudflare-one/team-and-resources/devices/cloudflare-one-client/)

我当时用第三方 WARP 脚本安装了 WireProxy，最终得到一个只监听本机的 SOCKS5：

```text
127.0.0.1:40000
```

安装方法可能随项目更新而变化，所以这里不照抄当时的菜单步骤。真正要确认的只有两件事：WireProxy 能使用 WARP 配置联网，并且 SOCKS 只绑定 `127.0.0.1`，不要把无认证代理暴露到公网。

## 先验证这条旁路真的可用

确认监听端口：

```bash
ss -lntp | grep 40000
```

然后分别检查普通出口和 SOCKS 出口：

```bash
curl https://www.cloudflare.com/cdn-cgi/trace | grep warp
curl --socks5-hostname 127.0.0.1:40000 \
  https://www.cloudflare.com/cdn-cgi/trace | grep warp
```

在这种只给特定流量使用 WireProxy 的结构里，第一条显示 `warp=off` 是正常的，第二条才应该显示 `warp=on`。我一开始也被这里绕进去过：`warp-cli connect` 的状态和系统普通请求是否经过本地 SOCKS，并不是一回事。

再直接测试 Gmail 的 IMAP 目标：

```bash
timeout 10 curl -v --socks5-hostname 127.0.0.1:40000 \
  telnet://imap.gmail.com:993
```

只要输出中出现 `SOCKS5 request granted`，并且成功连接到 `imap.gmail.com:993`，这条备用路径就通了。

## 给 Xray 增加一个 SOCKS 出站

我的 Xray 是脚本安装的，折腾期间先后碰到过 `/usr/local/etc/xray/config.json` 和 `/etc/xray/config.json` 两种路径。不同脚本版本的目录和 systemd 启动参数可能不一样，别凭印象修改；先用 `systemctl cat xray` 看清服务实际加载的是哪一份配置，并留好备份。

在 `outbounds` 数组里增加：

```json
{
  "tag": "warp-socks",
  "protocol": "socks",
  "settings": {
    "servers": [
      {
        "address": "127.0.0.1",
        "port": 40000
      }
    ]
  }
}
```

Xray 官方文档支持这种 [SOCKS 出站](https://xtls.github.io/en/config/outbounds/socks.html)。它只定义了一条可选出口，还不会改变现有流量。

接着在 `routing.rules` 靠前的位置加入 Gmail 规则：

```json
{
  "type": "field",
  "domain": [
    "full:imap.gmail.com",
    "full:smtp.gmail.com",
    "full:imap.googlemail.com",
    "full:smtp.googlemail.com"
  ],
  "port": "465,587,993",
  "network": "tcp",
  "outboundTag": "warp-socks"
}
```

我实际使用时只按域名匹配；整理这篇记录时补上了端口和 TCP 限制，范围更接近原始需求。Xray 会从上到下检查规则，命中第一条有效规则后就交给对应的 `outboundTag`，所以这条规则要放在可能提前吃掉 Gmail 流量的宽泛规则之前。`full:` 则是精确域名匹配。[Xray 路由文档](https://xtls.github.io/en/config/routing.html)

没有命中规则的流量会使用第一个出站，因此原本的 `direct` 仍应放在默认位置。这样 Gmail 邮件连接绕到 WARP，网页和其他服务继续使用 VPS 出口。

## 重启前别省略校验

下面以 `/etc/xray/config.json` 为例。先备份，再检查 JSON：

```bash
cp /etc/xray/config.json \
  /etc/xray/config.json.before-gmail-warp
jq empty /etc/xray/config.json
```

`jq` 只能检查 JSON 语法。还应该根据 `systemctl cat xray` 里真实的 `ExecStart`，调用同一个 Xray 可执行文件做配置测试。确认无误后再重启：

```bash
systemctl restart xray
journalctl -u xray -n 50 --no-pager
```

如果当前 SSH 或本机代理正依赖这项 Xray 服务，重启可能让连接瞬间断开。我后来修改配置时会保留第二个 SSH 会话，或者干脆只改好并校验，等自己方便时再手动重启。

服务恢复后，回到邮件 App 检查 Gmail 是否在线，最好再做一次真实的收信和发信测试。

## 后来它为什么又坏了

几天后服务器重启，Gmail 再次离线。我先怀疑切换 Xray 协议时覆盖了手工配置，但检查结果完全不是这样：

- Gmail 规则和 `warp-socks` 出站都还在；
- WireProxy 已开机启动，也在监听 `127.0.0.1:40000`；
- WireGuard 日志却反复握手失败，经过 SOCKS 的请求全部超时；
- 此时 VPS 直连 Gmail 的 993、465 和 587 已经全部恢复。

换句话说，Xray 正确命中了规则，然后把 Gmail 送进了一条已经断掉的旁路。曾经的修复，反而成了新的故障点。

我最后删除 Gmail 指向 `warp-socks` 的路由规则，让邮件重新直连。重启 Xray 后，macOS 邮件 App 马上恢复。WireProxy 和出站配置先留了几天作为退路，确认收发一直正常后再清理。

## 留给下次的判断表

以后再碰到类似问题，我会先测两条路径：

| VPS 直连 | WARP SOCKS | 应该怎么做 |
|---|---|---|
| 失败 | 成功 | 保留 Gmail 特殊分流 |
| 成功 | 失败 | 删除分流，或修复 WARP |
| 成功 | 成功 | 优先直连，少一个依赖 |
| 失败 | 失败 | 继续查上游网络、DNS 和 WARP 隧道 |

如果两条服务器路径都正常，邮件 App 仍然离线，再回头检查账号授权、客户端配置和本机代理才比较划算。
