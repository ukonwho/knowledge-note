
这次酝酿了很久想给大家讲一些关于Kaggle那点儿事，帮助对数据科学(Data Science)有兴趣的同学们更好的了解这个平台，最好能亲身参与进来，体会一下学校所学的东西和想要解决一个实际的问题所需要的能力的差距。虽然不是Data Science出身，但本着严谨的科研态度，在进行了大量的调研、学习以及对相关经验者的访谈之后，决定写下这篇专栏，一方面让那些对数据科学（Data Science）有兴趣的求职者和申请者能真正了解这个项目，另一方面也让那些有想法参与进来的人get到正确的打开方式。
注：此文章只允许ApplySquare（申请方）的相关媒体转账，其他不给予转载权。 

## 什么是Kaggle？
Kaggle成立于2010年，是一个进行数据发掘和预测竞赛的在线平台。从公司的角度来讲，可以提供一些数据，进而提出一个实际需要解决的问题；从参赛者的角度来讲，他们将组队参与项目，针对其中一个问题提出解决方案，最终由公司选出的最佳方案可以获得5K-10K美金的奖金。
除此之外，Kaggle官方每年还会举办一次大规模的竞赛，奖金高达一百万美金，吸引了广大的数据科学爱好者参与其中。从某种角度来讲，大家可以把它理解为一个众包平台，类似国内的猪八戒。但是不同于传统的低层次劳动力需求，Kaggle一直致力于解决业界难题，因此也创造了一种全新的劳动力市场——不再以学历和工作经验作为唯一的人才评判标准，而是着眼于个人技能，为顶尖人才和公司之间搭建了一座桥梁。

这里有一篇对Kaggle首席科学家Jeremy Howard的采访，介绍了Kaggle的创建初衷及运营模式，即任用最聪明的人解决世界上最棘手的问题；同时，任何公司和组织都可以受益于机器学习的发展进步，感兴趣的同学可以[戳这里：原文链接，来进一步了解。](https://link.zhihu.com/?target=http%3A//www.sramanamitra.com/2013/03/09/thought-leaders-in-big-data-interview-with-jeremy-howard-president-and-chief-scientist-of-kaggle-part-1/)

## Kaggle的竞赛模式是什么样的？
Kaggle上的竞赛有各种分类，例如奖金极高竞争激烈的的 “Featured”，相对平民化的 “Research”等等。但他们整体的项目模式是一样的，就是通过出题方给予的训练集建立模型，再利用测试集算出结果用来评比。同时，每个进行中的竞赛项目都会显示剩余时间、参与的队伍数量以及奖金金额，并且还会实时更新选手排位。在截止日期之前，所有队伍都可以自由加入竞赛，或者对已经提交的方案进行完善，因此排名也会不断变动，不到最后一刻谁都不知道花落谁家。

由于这类问题并没有标准答案，只有无限逼近最优解，所以这样的模式可以激励参与者提出更好的方案，甚至推动整个行业的发展。

Kaggle竞赛另一个有趣的地方在于每个人都有自己的Profile，上面会显示所有自己参与过的项目、活跃度、实时排位、历史最佳排位等，不仅看上去非常有成就感，更能在求职和申请的时候起到Certificate的作用。

Kaggle参赛者的背景大多是什么样的？

从比赛目标出发，参赛者主要分为两种，一种是以奖金和排名为目的，包括靠奖金为生的职业Kaggler；另外一种就是以提升相关skills和背景为目的业余爱好者甚至在校学生了。

从背景来看，前者的来源主要有丰富data science、data mining、machine learning工作经验的业内人士，或者是实力强劲的民间“技术宅”；而后者则往往是一些有一定技术能力，但经验欠缺，从中进行学习和锻炼的“长江后浪”。

## 0基础的人如何上手Kaggle？

理论上来讲，Kaggle欢迎任何数据科学的爱好者，不过实际上，要想真的参与其中，还是有一定门槛的。一般来讲，参赛者最好具有统计、计算机或数学相关背景，有一定的coding技能，对机器学习和深度学习有基本的了解。Kaggle任务虽然不限制编程语言，但绝大多数队伍会选用Python和R，所以你应该至少熟悉其中一种。此外，对于那些对成绩有追求的人，Feature Engineering也是必不可少的。但对于Data Science的入门者来说，这样的要求实在是有些过分了。对于这一块想要进一步了解的同学可以看这个问题：[特征工程到底是什么？](https://www.zhihu.com/question/29316149)其中[@城东](http://www.zhihu.com/people/jasonfreak) 的答案（[点这里](https://www.zhihu.com/question/29316149/answer/110159647)）和[@张戎](http://www.zhihu.com/people/zr9558) 的答案（[点这里](https://www.zhihu.com/question/29316149/answer/82949813)）都非常详细。

当然，如果你从未独立做过一个项目，还是要从练习赛开始熟悉。因为竞赛模式中的任务是公司悬赏发布的实际案例，并没有标准的答案；而练习赛不仅项目难度低，而且是有官方给出的参考方案的，大家可以用来对比改善自己的测试结果，从中进行提高。所以呢，建议感兴趣的同学先去独立做一下101和playground的训练赛，至于做多少个案例才能上道，就要看个人素质啦。这里为大家推荐几篇非常好的文章，里面手把手的教了大家入门级的三个经典练习项目，供大家学习。

1. Titanic（泰坦尼克之灾）
中文教程：[逻辑回归应用之Kaggle泰坦尼克之灾](https://link.zhihu.com/?target=http%3A//blog.csdn.net/han_xiaoyang/article/details/49797143)
英文教程：[An Interactive Data Science Tutorial](https://link.zhihu.com/?target=https%3A//www.kaggle.com/helgejo/titanic/an-interactive-data-science-tutorial)

2. House Prices: Advanced Regression Techniques（房价预测）
中文教程：[Kaggle竞赛 — 2017年房价预测](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/irenelin/p/7400388.html)
英文教程：[How to get to TOP 25% with Simple Model using sklearn](https://link.zhihu.com/?target=https%3A//www.kaggle.com/neviadomski/house-prices-advanced-regression-techniques/how-to-get-to-top-25-with-simple-model-sklearn)

3. Digital Recognition（数字识别）
中文教程：[大数据竞赛平台—Kaggle 入门 ](https://link.zhihu.com/?target=https%3A//www.kaggle.com/neviadomski/house-prices-advanced-regression-techniques/how-to-get-to-top-25-with-simple-model-sklearn)
英文教程：[Interactive Intro to Dimensionality Reduction](https://link.zhihu.com/?target=https%3A//www.kaggle.com/arthurtok/digit-recognizer/interactive-intro-to-dimensionality-reduction)

## Kaggle竞赛获奖及取得名次难么？

Kaggle竞赛取得奖金乃至取得好的名次的难度都是非常高的，通常一个项目的参与人数都能达到数千人，而其中只有Top 1可以得到奖金，可以说是高手中的高手。通常来说，几个具有一定水平的业内人士在临时组队的情况下最多也就拿到20名左右的成绩，想要再往前冲往往都需要有一定程度的默契和合作经验了。



所以，对于以学习与实践为目的的小白选手来说，不要太在意排名，从参赛的过程中不断地提升自己才是最终的目的。当经过一次又一次的洗礼最终取得一个不错的成绩后，相信你也已经成长为可以在相关领域独当一面的人才了。

## Kaggle竞赛的认可度高么？

Kaggle作为Data Science业内享有盛名的平台，在业界拥有极高的认可度。所以如果你是想寻找相关行业的工作，那一个漂亮的Kaggle profile将为你的简历增色不少。Quora上的这个问题：[How can we use Kaggle? （点击查看）](https://link.zhihu.com/?target=https%3A//www.quora.com/How-can-we-use-kaggle)就提到，把Kaggle的项目经验写在Linkedin上可以很直观的展现自己作为一个Data Scientist的能力。

国内亦有一些高级人才对Kaggle有很高的认知度，比如[Edward.Fu - 知乎](https://www.zhihu.com/people/edward-fu-91/answers) 一直在知乎各个和Kaggle相关的问题下留言寻觅Kaggle比赛经验丰富的人，表示常年有这方面的需求，说明国内对Kaggle的项目经验也是非常认可的。[@Lau Phunter](https://zhuanlan.zhihu.com/goog_1287543502)在[Kaggle 的比赛在 Machine Learning 领域中属于什么地位？](https://www.zhihu.com/question/32032932) 回答下面所说的：

写上参加过Kaggle比赛，我会看简历。
得过一次10%，我会给电话面试。
得过2次或者以上10%，我会给on site面试。
得过一次前10，我们会谈笑风生。
参加Kaggle是一种怎样的体验？

在调研的过程中我采访了几个Kaggler，将他们的亲身经验做了一下总结：

Kaggler A，NYC Data Science Academy team leader/ 美国数据电子交易公司CEO，多次参加Kaggle比赛：

参加此项目，你不可或缺的品质就是持续的热情和坚韧不拔的毅力，即使是像我这样的老司机，和另外两个专攻CS和统计方向的小伙伴组队，一个难度中等的项目做下来也要投入两周，每天工作10h以上。更别提那些有着强迫症，一遍遍修改方案，直至deadline的完美主义大牛了。我相信没有一支夺冠队伍是在提交方案后完全没改过的，顶尖高手的成功不仅是基于他们的专业素养，还有其背后我们看不到的勤奋。
Kaggler B，某知名大数据公司的数据分析师，在美国读统计研究生期间曾通过Kaggle项目提升自己数据操作技能：

我是统计本科申请一年半的统计Master，目前刚刚回国工作。在出国前对Kaggle也是闻所未闻，来到美国以后，在导师的引导下知道了Kaggle这个巨大的学习源，经常在上面学习。在我看来，Kaggle的背书还是非常有用的，排位前几十的都是大神级别，他们从来不需要找工作，都是工作来找他们。而对我们这样的小白，如果没有整块时间找实习或者没有找到合适的实习机会，利用闲暇时间做一些Kaggle项目，写在简历上也能算做一些项目经验，更容易得到面试；同时，在做项目的过程中，实实在在的Skills的提高也能让我们在求职时笔试的表现更好，获得更好的工作机会。
除此之外，知乎上面著名的“体验贴”也给出了很多第一手的体验：[参加kaggle竞赛是怎样一种体验？ - 大数据 - 知乎。](https://www.zhihu.com/question/24533374)在这个问题下 [Naiyan Wang](https://www.zhihu.com/people/naiyan-wang/answers) 给出了一个非常详细的答案，同时答主也有一个很好的Profile，文中涉及Kaggle侧重的能力，比赛的要点，以及关键的技术，欢迎大家围观~ 

Kaggle的竞争非常激烈，正如[OFuture T - 知乎](https://www.zhihu.com/people/ofuture-t/answers) 所说，很多时候Kaggle的排名即便是前50位流动性也很大，从前几名跌至几十名不过一两天的事，可想而知想要保住排位要在此付出多大的时间和精力，一次次的推翻自己，碾压别人，真是个磨人的小妖精。。。

## Kaggle有什么意义？



从求职者的角度来看：
Kaggle提供了一个非常好的学习平台，在这里你可以接触到真正的业界案例，收获实际的项目经验，在每一个项目中不断挑战自己，甚至在Kaggle榜上占据一席之位，提高自己在业内的知名度，优秀的排位甚至可能带来的非常好的工作机会。同时，也可以认识一群志同道合的人，扩展自己的professional network，与业内最顶尖的高手互动，尤其是很多队伍在比赛结束后都会公开自己的解法，如果这个项目恰好你参与过，为之投入过无数个日日夜夜，此时就是不可多得的学习机会。

对于刚刚进入这个行业的菜鸟而言，参加Kaggle的项目是非常“长见识”的，可能初期的尝试会非常吃力，毕竟都是非常前沿的问题，但是如果能坚持完整的把一个项目做下来，且不说coding能力会有一个很大的提高，在实际案例中解决问题的能力也会得到极大的锻炼，为自己的职业生涯打下一个良好的基础。如果能在Kaggle这种高手云集的比赛中获得一个还不错的成绩，写在简历上足以打动你今后的Boss，跳槽就翻倍的高薪工作指日可待！值得一提的是，虽然是汇集精英的社区，Kaggle的论坛氛围很好，对新人非常友好，大家一定要多看Script多请教！



从留学申请者的角度来看：


对于申请Data Science相关专业的同学来讲，大数据的走红使得Data Science的申请竞争愈演愈烈，因此如何提升背景也是大家非常关心的问题。而Kaggle正好给大家提供了一个非常好的平台，在这里人人有参与项目的机会，无论你的背景是什么，都可以通过选择合适的项目来找到属于自己的位置，利用自己的专业优势，为整个team作出贡献，丰富简历的同时也能学习一些干货，为自己以后的学习打好基础。而其在领域内的知名度足以让你在众多申请者中脱颖而出，绝对是申请利器！

对于新人，如何在Kaggle中提升排位？



选择合适的队友：


由于Kaggle的项目是由公司提供的，涉及各个行业，所以一般都是不同背景的人组队参加（如统计、CS、DS，项目相关领域如生物等）。因此对于新手来讲，很重要的一点就是要抱好大腿，不仅可以蹭到好的排名，还有机会近距离向大牛学习，技能值必然嗖嗖涨。而自己可以从力所能及的工作做起，如清洗数据等等，积累项目经验。

选择“正确”的项目；
首先，选择数据量小的项目，这样不管使用什么算法都不会耗时太久，对机器性能要求也不高，出结果也比较快；其次，选择难度低奖金少的项目，一方面竞争小，另一方面也适合新手；最后，选择参与人数多的项目，毕竟有那么多“僵尸号”撑着。这样下来，基本上认认真真做下来排名都不会太难看。



选择恰当的工具：


我们都知道循序渐进的道理，因此对于刚刚涉猎Kaggle，只是希望从中学习，而不追求高排名的同学，可以先从学习Machine Learning中常用的模型开始，比如Logistic Regression和Random Forest，这两个模型对于大部分问题就够了；基础好的还可以学习一下Gradient Boosting，虽然难度高一点，但是可视化效果会好很多。

当然，说到底，想获得更好的名次，提高自己的Skills才是终极解决方案！



最后是彩蛋时间：

Data Science专业群：
我们准备了Data Science相关的专业群，给准备留学申请DS专业的小伙伴一个聚集地。

群里的福利：

✦ Program信息
我们会帮助大家分析最新最热的DS Program申请信息，帮助大家选择最适合自己的项目。

✦ 神秘嘉宾分享
我们会邀请资深数据科学家作为嘉宾来跟大家进行语音分享，谈一谈有关于这个领域背景提升、申请和就业的一系列问题。

✦ 组队打怪
你可以找到志同道合的小伙伴，一起组团做project，互通有无share有用信息，在崎岖的申请路上互相取暖。

详细信息及报名方式查看这里：老师，我也想申请Data Science呢！

学习资源：
给大家汇总了一些超级良心的手把手教程，
@Wille
 在专栏中发表的文章—Kaggle 入门指南， 详细介绍了Kaggle项目的大致流程，包括Data Exploration, Statistical Test, Data Processing, Feature Engineering, Model Selection, Ensemble Generation每一步该怎么做，有哪些Tips，最后还给出了一个“Home Depot Search Relevance”的案例，拿到它就可以开始自己的Kaggle排位赛了！祝愿大家都能够成为一个优秀的Data Scientist！

接下来是我整理的一些相关的学习资源，大家各取所需。



基础准备篇之Python
[怎么用最短时间高效而踏实地学习 Python？](https://www.zhihu.com/question/28530832)

[你是如何自学 Python 的？](https://www.zhihu.com/question/20702054)

[在线教育网站（Coursera网易云edx课堂腾讯课堂等）有哪些值得推荐的 Python 教程？](https://www.zhihu.com/question/46835030)

基础准备篇之R
[业余时间如何学数据分析？ 如何高效地学好 R？ 好看的数据可视化的图片是怎么样做的？](https://www.zhihu.com/question/22119753)



基础准备篇之Machine Learning
[机器学习该怎么入门？ 深度学习如何入门？ JustFollowUs/Machine-Learning](https://link.zhihu.com/?target=https%3A//github.com/JustFollowUs/Machine-Learning)



基础准备篇之Kaggle Experience
[从Python菜鸟到Python Kaggler的过程：](https://link.zhihu.com/?target=http%3A//dataunion.org/9805.html%3Futm_source%3Dtuicool)

[Python机器学习实践与Kaggle实战](https://link.zhihu.com/?target=https%3A//mlnote.wordpress.com/2015/12/16/python%25E6%259C%25BA%25E5%2599%25A8%25E5%25AD%25A6%25E4%25B9%25A0%25E5%25AE%259E%25E8%25B7%25B5%25E4%25B8%258Ekaggle%25E5%25AE%259E%25E6%2588%2598-machine-learning-for-kaggle-competition-in-python/)

[经常更新的的大数据博客](https://link.zhihu.com/?target=http%3A//www.36dsj.com/archives/9991)

[TO最爱学习的你：国外大数据博客资源大全 | 36大数据](https://link.zhihu.com/?target=http%3A//www.36dsj.com/archives/9991)

[How to start doing Kaggle competitions？](https://link.zhihu.com/?target=https%3A//www.quora.com/How-do-I-start-doing-Kaggle-competitions)

[What do top Kaggle competitors focus on?](https://link.zhihu.com/?target=https%3A//www.quora.com/What-do-top-Kaggle-competitors-focus-on)

[A Journey Into Data Science](https://link.zhihu.com/?target=https%3A//ajourneyintodatascience.quora.com/)

[Techniques to improve the accuracy of your Predictive Models](https://link.zhihu.com/?target=http%3A//anotherdataminingblog.blogspot.com.au/2013/10/techniques-to-improve-accuracy-of-your_17.html)