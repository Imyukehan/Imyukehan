---
title: Who does that server really serve?
---

**Richard Stallman**

> (From [GNU PHILOSOPHY](https://www.gnu.org/philosophy/who-does-that-server-really-serve.en.html).)

**On the Internet, proprietary software isn't the only way to lose your freedom. Service as a Software Substitute, or SaaSS, is another way to give someone else power over your computing.**

<!-- More -->

The basic point is, you can have control over a program someone else wrote (if it's free), but you can never have control over a service someone else runs, so never use a service where in principle a program would do.

SaaSS means using a service implemented by someone else as a substitute for running your copy of a program. The term is ours; articles and ads won't use it, and they won't tell you whether a service is SaaSS. Instead they will probably use the vague and distracting term “cloud”, which lumps SaaSS together with various other practices, some abusive and some ok. With the explanation and examples in this page, you can tell whether a service is SaaSS.

### Background: How Proprietary Software Takes Away Your Freedom

Digital technology can give you freedom; it can also take your freedom away. The first threat to our control over our computing came from *proprietary software*: software that the users cannot control because the owner (a company such as Apple or Microsoft) controls it. The owner often takes advantage of this unjust power by inserting malicious features such as spyware, back doors, and [Digital Restrictions Management (DRM)](http://defectivebydesign.org/) (referred to as “Digital Rights Management” in their propaganda).

Our solution to this problem is developing *free software* and rejecting proprietary software. Free software means that you, as a user, have four essential freedoms: (0) to run the program as you wish, (1) to study and change the source code so it does what you wish, (2) to redistribute exact copies, and (3) to redistribute copies of your modified versions. (See the [free software definition](https://www.gnu.org/philosophy/free-sw.html).)

With free software, we, the users, take back control of our computing. Proprietary software still exists, but we can exclude it from our lives and many of us have done so. However, we are now offered another tempting way to cede control over our computing: Service as a Software Substitute (SaaSS). For our freedom's sake, we have to reject that too.

### How Service as a Software Substitute Takes Away Your Freedom

Service as a Software Substitute (SaaSS) means using a service as a substitute for running your copy of a program. Concretely, it means that someone sets up a network server that does certain computing tasks—for instance, modifying a photo, translating text into another language, etc.—then invites users to do computing via that server. A user of the server would send her data to the server, which does *her own computing* on the data thus provided, then sends the results back to her or acts directly on her behalf.

The computing is *her own* because, by assumption, she could, in principle, have done it by running a program on her own computer (whether or not that program is available to her at present). In cases where this assumption is not so, it isn't SaaSS.

These servers wrest control from the users even more inexorably than proprietary software. With proprietary software, users typically get an executable file but not the source code. That makes it hard to study the code that is running, so it's hard to determine what the program really does, and hard to change it.

With SaaSS, the users do not have even the executable file that does their computing: it is on someone else's server, where the users can't see or touch it. Thus it is impossible for them to ascertain what it really does, and impossible to change it.

Furthermore, SaaSS automatically leads to consequences equivalent to the malicious features of certain proprietary software.

For instance, some proprietary programs are “spyware”: the program [sends out data about users' computing activities](https://www.gnu.org/philosophy/proprietary-surveillance.html). Microsoft Windows sends information about users' activities to Microsoft. Windows Media Player reports what each user watches or listens to. The Amazon Kindle reports which pages of which books the user looks at, and when. Angry Birds reports the user's geolocation history.

Unlike proprietary software, SaaSS does not require covert code to obtain the user's data. Instead, users must send their data to the server in order to use it. This has the same effect as spyware: the server operator gets the data—with no special effort, by the nature of SaaSS. Amy Webb, who intended never to post any photos of her daughter, made the mistake of using SaaSS (Instagram) to edit photos of her. Eventually [they leaked from there](http://www.slate.com/articles/technology/data_mine_1/2013/09/privacy_facebook_kids_don_t_post_photos_of_your_kids_on_social_media.html).

Theoretically, homomorphic encryption might some day advance to the point where future SaaSS services might be constructed to be unable to understand some of the data that users send them. Such services *could* be set up not to snoop on users; this does not mean they *will* do no snooping.

Some proprietary operating systems have a universal back door, permitting someone to remotely install software changes. For instance, Windows has a universal back door with which Microsoft can forcibly change any software on the machine. Nearly all portable phones have them, too. Some proprietary applications also have universal back doors; for instance, the Steam client for GNU/Linux allows the developer to remotely install modified versions.

With SaaSS, the server operator can change the software in use on the server. He ought to be able to do this, since it's his computer; but the result is the same as using a proprietary application program with a universal back door: someone has the power to silently impose changes in how the user's computing gets done.

Thus, SaaSS is equivalent to running proprietary software with spyware and a universal back door. It gives the server operator unjust power over the user, and that power is something we must resist.

### SaaSS and SaaS

Originally we referred to this problematical practice as “SaaS”, which stands for “Software as a Service”. It's a commonly used term for setting up software on a server rather than offering copies of it to users, and we thought it described precisely the cases where this problem occurs.

Subsequently we became aware that the term SaaS is sometimes used for communication services—activities for which this issue is not applicable. In addition, the term “Software as a Service” doesn't explain *why* the practice is bad. So we coined the term “Service as a Software Substitute”, which defines the bad practice more clearly and says what is bad about it.

### Untangling the SaaSS Issue from the Proprietary Software Issue

SaaSS and proprietary software lead to similar harmful results, but the mechanisms are different. With proprietary software, the mechanism is that you have and use a copy which is difficult and/or illegal to change. With SaaSS, the mechanism is that you don't have the copy that's doing your computing.

These two issues are often confused, and not only by accident. Web developers use the vague term “web application” to lump the server software together with programs run on your machine in your browser. Some web pages install nontrivial, even large JavaScript programs into your browser without informing you.  [When these JavaScript programs are nonfree](https://www.gnu.org/philosophy/javascript-trap.html), they cause the same sort of injustice as any other nonfree software. Here, however, we are concerned with the issue of using the service itself.

Many free software supporters assume that the problem of SaaSS will be solved by developing free software for servers. For the server operator's sake, the programs on the server had better be free; if they are proprietary, their developers/owners have power over the server. That's unfair to the server operator, and doesn't help the server's users at all. But if the programs on the server are free, that doesn't protect *the server's users* from the effects of SaaSS. These programs liberate the server operator, but not the server's users.

Releasing the server software source code does benefit the community: it enables suitably skilled users to set up similar servers, perhaps changing the software.  [We recommend using the GNU Affero GPL](https://www.gnu.org/licenses/license-recommendations.html) as the license for programs often used on servers.

But none of these servers would give you control over computing you do on it, unless it's *your* server (one whose software load you control, regardless of whether the machine is your property). It may be OK to trust your friend's server for some jobs, just as you might let your friend maintain the software on your own computer. Outside of that, all these servers would be SaaSS for you. SaaSS always subjects you to the power of the server operator, and the only remedy is, *Don't use SaaSS!* Don't use someone else's server to do your own computing on data provided by you.

This issue demonstrates the depth of the difference between “open” and “free”. Source code that is open source [is, nearly always, free](https://www.gnu.org/philosophy/free-open-overlap.html). However, the idea of an [“open software” service](http://opendefinition.org/software-service), meaning one whose server software is open source and/or free, fails to address the issue of SaaSS.

Services are fundamentally different from programs, and the ethical issues that services raise are fundamentally different from the issues that programs raise. To avoid confusion, we [avoid describing a service as “free” or “proprietary.”](https://www.gnu.org/philosophy/network-services-arent-free-or-nonfree.html)

### Distinguishing SaaSS from Other Network Services

Which online services are SaaSS? The clearest example is a translation service, which translates (say) English text into Spanish text. Translating a text for you is computing that is purely yours. You could do it by running a program on your own computer, if only you had the right program. (To be ethical, that program should be free.) The translation service substitutes for that program, so it is Service as a Software Substitute, or SaaSS. Since it denies you control over your computing, it does you wrong.

Another clear example is using a service such as Flickr or Instagram to modify a photo. Modifying photos is an activity that people have done in their own computers for decades; doing it in a server you don't control, rather than your own computer, is SaaSS.

Rejecting SaaSS does not mean refusing to use any network servers run by anyone other than you. Most servers are not SaaSS because the jobs they do are some sort of communication, rather than the user's own computing.

The original idea of web servers wasn't to do computing for you, it was to publish information for you to access. Even today this is what most web sites do, and it doesn't pose the SaaSS problem, because accessing someone's published information isn't doing your own computing. Neither is use of a blog site to publish your own works, or using a microblogging service such as Twitter or StatusNet. (These services may or may not have other problems, depending on details.) The same goes for other communication not meant to be private, such as chat groups.

In its essence, social networking is a form of communication and publication, not SaaSS. However, a service whose main facility is social networking can have features or extensions which are SaaSS.

If a service is not SaaSS, that does not mean it is OK. There are other ethical issues about services. For instance, Facebook distributes video in Flash, which pressures users to run nonfree software; it requires running nonfree JavaScript code; and it gives users a misleading impression of privacy while luring them into baring their lives to Facebook. Those are important issues, different from the SaaSS issue.

Services such as search engines collect data from around the web and let you examine it. Looking through their collection of data isn't your own computing in the usual sense—you didn't provide that collection—so using such a service to search the web is not SaaSS. However, using someone else's server to implement a search facility for your own site *is* SaaSS.

Purchasing online is not SaaSS, because the computing isn't *your own* activity; rather, it is done jointly by and for you and the store. The real issue in online shopping is whether you trust the other party with your money and other personal information (starting with your name).

Repository sites such as Savannah and SourceForge are not inherently SaaSS, because a repository's job is publication of data supplied to it.

Using a joint project's servers isn't SaaSS because the computing you do in this way isn't your own. For instance, if you edit pages on Wikipedia, you are not doing your own computing; rather, you are collaborating in Wikipedia's computing. Wikipedia controls its own servers, but organizations as well as individuals encounter the problem of SaaSS if they do their computing in someone else's server.

Some sites offer multiple services, and if one is not SaaSS, another may be SaaSS. For instance, the main service of Facebook is social networking, and that is not SaaSS; however, it supports third-party applications, some of which are SaaSS. Flickr's main service is distributing photos, which is not SaaSS, but it also has features for editing photos, which is SaaSS. Likewise, using Instagram to post a photo is not SaaSS, but using it to transform the photo is SaaSS.

Google Docs shows how complex the evaluation of a single service can become. It invites people to edit a document by running a large [nonfree JavaScript program](https://www.gnu.org/philosophy/javascript-trap.html), clearly wrong. However, it offers an API for uploading and downloading documents in standard formats. A free software editor can do so through this API. This usage scenario is not SaaSS, because it uses Google Docs as a mere repository. Showing all your data to a company is bad, but that is a matter of privacy, not SaaSS; depending on a service for access to your data is bad, but that is a matter of risk, not SaaSS. On the other hand, using the service for converting document formats *is* SaaSS, because it's something you could have done by running a suitable program (free, one hopes) in your own computer.

Using Google Docs through a free editor is rare, of course. Most often, people use it through the nonfree JavaScript program, which is bad like any nonfree program. This scenario might involve SaaSS, too; that depends on what part of the editing is done in the JavaScript program and what part in the server. We don't know, but since SaaSS and proprietary software do similar wrong to the user, it is not crucial to know.

Publishing via someone else's repository does not raise privacy issues, but publishing through Google Docs has a special problem: it is impossible even to *view the text* of a Google Docs document in a browser without running the nonfree JavaScript code. Thus, you should not use Google Docs to publish anything—but the reason is not a matter of SaaSS.

The IT industry discourages users from making these distinctions. That's what the buzzword “cloud computing” is for. This term is so nebulous that it could refer to almost any use of the Internet. It includes SaaSS as well as many other network usage practices. In any given context, an author who writes “cloud” (if a technical person) probably has a specific meaning in mind, but usually does not explain that in other articles the term has other specific meanings. The term leads people to generalize about practices they ought to consider individually.

If “cloud computing” has a meaning, it is not a way of doing computing, but rather a way of thinking about computing: a devil-may-care approach which says, “Don't ask questions. Don't worry about who controls your computing or who holds your data. Don't check for a hook hidden inside our service before you swallow it. Trust companies without hesitation.” In other words, “Be a sucker.” A cloud in the mind is an obstacle to clear thinking. For the sake of clear thinking about computing, let's avoid the term “cloud.”

### Renting a Server Distinguished from SaaSS

If you rent a server (real or virtual), whose software load you have control over, that's not SaaSS. In SaaSS, someone else decides what software runs on the server and therefore controls the computing it does for you. In the case where you install the software on the server, you control what computing it does for you. Thus, the rented server is virtually your computer. For this issue, it counts as yours.

The *data* on the rented remote server is less secure than if you had the server at home, but that is a separate issue from SaaSS.

### Dealing with the SaaSS Problem

Only a small fraction of all web sites do SaaSS; most don't raise the issue. But what should we do about the ones that raise it?

For the simple case, where you are doing your own computing on data in your own hands, the solution is simple: use your own copy of a free software application. Do your text editing with your copy of a free text editor such as GNU Emacs or a free word processor. Do your photo editing with your copy of free software such as GIMP. What if there is no free program available? A proprietary program or SaaSS would take away your freedom, so you shouldn't use those. You can contribute your time or your money to development of a free replacement.

What about collaborating with other individuals as a group? It may be hard to do this at present without using a server, and your group may not know how to run its own server. If you use someone else's server, at least don't trust a server run by a company. A mere contract as a customer is no protection unless you could detect a breach and could really sue, and the company probably writes its contracts to permit a broad range of abuses. The state can subpoena your data from the company along with everyone else's, as Obama has done to phone companies, supposing the company doesn't volunteer them like the US phone companies that illegally wiretapped their customers for Bush. If you must use a server, use a server whose operators give you a basis for trust beyond a mere commercial relationship.

However, on a longer time scale, we can create alternatives to using servers. For instance, we can create a peer-to-peer program through which collaborators can share data encrypted. The free software community should develop distributed peer-to-peer replacements for important “web applications”. It may be wise to release them under the [GNU Affero GPL](https://www.gnu.org/licenses/why-affero-gpl.html), since they are likely candidates for being converted into server-based programs by someone else. The [GNU project](https://www.gnu.org/) is looking for volunteers to work on such replacements. We also invite other free software projects to consider this issue in their design.

In the meantime, if a company invites you to use its server to do your own computing tasks, don't yield; don't use SaaSS. Don't buy or install “thin clients”, which are simply computers so weak they make you do the real work on a server, unless you're going to use them with *your* server. Use a real computer and keep your data there. Do your own computing with your own copy of a free program, for your freedom's sake.