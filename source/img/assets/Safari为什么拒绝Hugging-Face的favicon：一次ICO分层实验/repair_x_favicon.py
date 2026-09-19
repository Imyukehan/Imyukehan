#!/usr/bin/env python3
"""Targeted workaround for a verified X favicon cache failure in Safari.
Default: inspect. Quit Safari before --apply or --undo BACKUP_DIRECTORY.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import time

ICON_URL = 'https://abs.twimg.com/favicons/twitter.3.ico'
APPLE_EPOCH = 978307200
DEFAULT_DB = Path.home() / 'Library/Safari/Favicon Cache/favicons.db'


def safari_closed():
    result = subprocess.run(['/usr/bin/pgrep', '-x', 'Safari'], capture_output=True)
    if result.returncode != 1:
        raise RuntimeError('请先用 ⌘Q 完全退出 Safari，然后再运行。')


def connect(path):
    con = sqlite3.connect(path.resolve().as_uri() + '?mode=rw', uri=True, timeout=5)
    for table, expected in {
        'icon_info': {'uuid', 'url', 'timestamp', 'width', 'height', 'has_generated_representations'},
        'rejected_resources': {'page_url', 'icon_url', 'timestamp'},
        'page_url': {'url', 'uuid'},
    }.items():
        actual = {r[1] for r in con.execute(f'PRAGMA table_info({table})')}
        if actual != expected:
            con.close()
            raise RuntimeError(f'数据库结构与已测试版本不同：{table}，已停止。')
    return con


def inspect(con, path):
    rows = con.execute('SELECT uuid,timestamp FROM icon_info WHERE url=?', (ICON_URL,)).fetchall()
    if len(rows) != 1:
        raise RuntimeError(f'找到 {len(rows)} 条 X 图标记录；本方案需要一条已有缓存记录，已停止。')
    uuid, timestamp = rows[0]
    icon = path.parent / 'favicons' / hashlib.md5(uuid.encode()).hexdigest().upper()
    if not icon.is_file() or not icon.stat().st_size:
        raise RuntimeError('现有图标文件缺失；更新时间无法修复缺失图片，已停止。')
    check = subprocess.run(['/usr/bin/sips', '-g', 'pixelWidth', '-g', 'pixelHeight', str(icon)], capture_output=True, text=True)
    if check.returncode or 'pixelWidth:' not in check.stdout or '<nil>' in check.stdout:
        raise RuntimeError('现有图标不能被系统读取，已停止。')
    rejections = con.execute('SELECT page_url,icon_url,timestamp FROM rejected_resources WHERE icon_url=?', (ICON_URL,)).fetchall()
    return {'uuid': uuid, 'timestamp': timestamp, 'rejections': rejections,
            'image_sha256': hashlib.sha256(icon.read_bytes()).hexdigest()}


def backup(con, root):
    root.mkdir(parents=True, exist_ok=True)
    directory = root / f'x-favicon-{time.time_ns()}'
    directory.mkdir(mode=0o700)
    with sqlite3.connect(directory / 'favicons.db') as copy:
        con.backup(copy)
    return directory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument('--apply', action='store_true')
    action.add_argument('--undo', type=Path, metavar='BACKUP_DIRECTORY')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    parser.add_argument('--backup-dir', type=Path, default=Path.home() / 'Downloads/Safari-favicon-backups')
    args = parser.parse_args()
    path = args.db.expanduser().resolve()
    if args.apply or args.undo:
        safari_closed()
    con = connect(path)
    try:
        state = inspect(con, path)
        print(f'X 图标文件可读，匹配拒绝记录：{len(state["rejections"])} 条。')
        if not args.apply and not args.undo:
            print('本次仅检查。修复：退出 Safari 后，加 --apply 再运行。')
            return
        undo = None
        if args.undo:
            undo = json.loads((args.undo / 'changes.json').read_text())
            if undo['database'] != str(path) or undo['icon_url'] != ICON_URL:
                raise RuntimeError('备份不属于这个数据库，已停止。')
            if state['uuid'] != undo['before']['uuid'] or state['timestamp'] != undo['new_timestamp']:
                raise RuntimeError('图标记录已再次变化，不能自动撤销，已停止。')
        directory = backup(con, args.backup_dir)
        safari_closed()
        con.execute('BEGIN IMMEDIATE')
        if inspect(con, path) != state:
            raise RuntimeError('检查后记录发生变化，已停止。')
        if undo:
            con.execute('UPDATE icon_info SET timestamp=? WHERE url=? AND uuid=?', (undo['before']['timestamp'], ICON_URL, state['uuid']))
            con.executemany('INSERT OR IGNORE INTO rejected_resources(page_url,icon_url,timestamp) VALUES(?,?,?)', undo['before']['rejections'])
        else:
            now = time.time() - APPLE_EPOCH
            changes = {'database': str(path), 'icon_url': ICON_URL, 'before': state, 'new_timestamp': now}
            (directory / 'changes.json').write_text(json.dumps(changes, ensure_ascii=False, indent=2))
            con.execute('UPDATE icon_info SET timestamp=? WHERE url=? AND uuid=?', (now, ICON_URL, state['uuid']))
            con.execute('DELETE FROM rejected_resources WHERE icon_url=?', (ICON_URL,))
        if con.execute('PRAGMA quick_check').fetchone()[0] != 'ok':
            raise RuntimeError('数据库校验未通过，已回滚。')
        con.commit()
        print('已撤销本次修改。' if undo else '已更新时间并清除匹配拒绝记录。现在可重新打开 Safari，访问一个此前没打开的推文检查图标。')
        print(f'数据库备份：{directory}')
        if not undo:
            print(f'撤销：退出 Safari 后，运行本脚本并加 --undo "{directory}"')
    finally:
        con.close()


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, sqlite3.Error, ValueError, KeyError) as error:
        raise SystemExit(f'停止：{error}')
