title: 执行上下文
date: 2018-03-27 21:51:33
author: 
  nick: mengro
  link: https://www.github.com/mengro
cover: https://github.com/mengro/mengro.github.io/blob/master/img/preview/javascript.png?raw=true
tags:
subtitle: your subtitle
---
******
###### 本文转自[这波能反杀](https://yangbo5207.github.io)的[执行上下文](https://yangbo5207.github.io/wutongluo/ji-chu-jin-jie-xi-lie/er-3001-zhi-xing-shang-xia-wen.html),非常推荐该作者的博客，也很感谢他的分享
<img src="static/images/executeContext/1.png">
* <b>什么是执行上下文？</b>

  可能很多人跟我一样对这个词有过困惑，但其实这个词就是它字面的意思：“当前代码的执行环境”，这是js基础中非常重要的一个概念，对于js执行过程的理解直观重要。那么在js中，执行环境又指的什么呢？

* <b>js的执行环境大致分为三种：</b>

  1.  全局环境：JavaScript代码运行起来会首先进入该环境
  2.  函数环境：当函数被调用执行时，会进入当前函数中执行代码
  3.  eval（不建议使用，可忽略）

  因此在一个JavaScript程序中，必定会产生多个执行上下文，JavaScript引擎会以栈的方式来处理它们，这个栈，我们称其为函数调用栈(call stack)。栈底永远都是全局上下文，而栈顶就是当前正在执行的上下文。

  当代码在执行过程中，遇到以上三种情况，都会生成一个执行上下文，放入栈中，而处于栈顶的上下文执行完毕之后，就会自动出栈。为了更加清晰的理解这个过程，根据下面的例子，结合图示给大家展示。

> 执行上下文可以理解为函数执行的环境，每一个函数执行时，都会给对应的函数创建这样一个执行环境。

```
var color = 'blue';

function changeColor() {
    var anotherColor = 'red';

    function swapColors() {
        var tempColor = anotherColor;
        anotherColor = color;
        color = tempColor;
    }

    swapColors();
}

changeColor();
```

我们用ECStack来表示处理执行上下文组的堆栈。我们很容易知道，第一步，首先是全局上下文入栈。

<center><img src="static/images/executeContext/2.png"></center>

全局上下文入栈之后，其中的可执行代码开始执行，直到遇到了changeColor()，这一句激活函数changeColor创建它自己的执行上下文，因此第二步就是changeColor的执行上下文入栈。

<center><img src="static/images/executeContext/3.png"></center>

changeColor的上下文入栈之后，控制器开始执行其中的可执行代码，遇到swapColors()之后又激活了一个执行上下文。因此第三步是swapColors的执行上下文入栈。

<center><img src="static/images/executeContext/4.png"></center>

在swapColors的可执行代码中，再没有遇到其他能生成执行上下文的情况，因此这段代码顺利执行完毕，swapColors的上下文从栈中弹出。

<center><img src="static/images/executeContext/5.png"></center>

swapColors的执行上下文弹出之后，继续执行changeColor的可执行代码，也没有再遇到其他执行上下文，顺利执行完毕之后弹出。这样，ECStack中就只身下全局上下文了。

<center><img src="static/images/executeContext/6.png"></center>

全局上下文在浏览器窗口关闭后出栈。

> 注意：函数中，遇到return能直接终止可执行代码的执行，因此会直接将当前上下文弹出栈。

<center><img src="static/images/executeContext/7.png"></center>

详细了解了这个过程之后，我们就可以对执行上下文总结一些结论了。

  * 单线程
  * 同步执行，只有栈顶的上下文处于执行中，其他上下文需要等待
  * 全局上下文只有唯一的一个，它在浏览器关闭时出栈
  * 函数的执行上下文的个数没有限制
  * 每次某个函数被调用，就会有个新的执行上下文为其创建，即使是调用的自身函数，也是如此。
  * 为了巩固一下执行上下文的理解，我们再来绘制一个例子的演变过程，这是一个简单的闭包例子。

```
function f1(){
  var n=999;
  function f2(){
      alert(n);
  }
  return f2;
}
var result=f1();
result(); // 999
```

因为f1中的函数f2在f1的可执行代码中，并没有被调用执行，因此执行f1时，f2不会创建新的上下文，而直到result执行时，才创建了一个新的。具体演变过程如下。

<center><img src="static/images/executeContext/8.png" alt='上例演变过程'></center>

最后留一个简单的例子，大家可以自己脑补一下这个例子在执行过程中执行上下文的变化情况。

```
var name = "window";

var p = {
  name: 'Perter',
  getName: function() {

    // 利用变量保存的方式保证其访问的是p对象
    var self = this;
    return function() {
      return self.name;
    }
  }
}

var getName = p.getName();
var _name = getName();
console.log(_name);
```