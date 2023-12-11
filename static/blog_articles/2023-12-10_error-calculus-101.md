Error Calculus 101
==================

Table of Contents
-----------------
[TOC]

Introduction. What is the point of error calculus
-------------------------------------------------

I studied Physics back in the days. One of the most useful things I took with me from 
that time is how to calculate and present uncertainties. The basics are pretty easy for any data 
scientist to learn, but it can make a massive difference. 

_That's just P-Values.... I know that.... Boooring!_

It's not. P-values tell you very little. Let's say we are working together on a model to predict
predict stock prices. Now I come to the daily and say that adding the new feature was 
significantly better with a p_value of 0.01. Awesome! But I have no idea how much improvement
I can expect. Tiny differences might be significant. 

But things get worse if the change you see is not significant. Then you might as well say:

_we tried the new feature but the dog ate our results_

Not 100% accurate but you get the point. Insignificant results essentially mean that we cannot 
confirm whether the model improved or not.

Now imagine I instead come to you and tell you:

_If we add the new feature, the model improves between 1 and 3%_

You suddenly know how big the effect most likely will be and the range, the improvement 
will likely fall into. Even better, you can get the p_values back if you really wanted to with a few simple rules. 
This is a confidence interval, or simply an "error" as we call them in physics. 

It's a much better way to communicate and helps comparing and aggregating experiments. 
I hope I convinced you to keep reading, so let's start with the basics.

What are confidence intervals?
------------------------------

Pretty simple. If you are measuring something that follows a distribution, then you can define 
a range in which X% of measurements will fall into. The most common Confidence interval is the 95% 
CL, but in physics, we usually used the 68% CL. 

<img src="/static/article_images/gaussian.png" alt="Gaussian Distribution" width="100%"/>

If you know your distributions, you'll know that these levels correspond to 1 and 2 standard deviations 
of the gauss distribution. So if we know the distribution of the thing we are measuring, we could produce something
like:

$$ \text{Improvement with Feature X} = 42 \pm 11 \% $$

The 42 tells is the value of what we measured, and the ± 11 tells in which range we expect
the value to lie in if we did the experiment again. 

If you are somewhat used to statistics and distributions, you might say. Looks easy enough 
, but this might get pretty difficult really fast depending of which kind of distributions 
you deal with. If that's the case I have good news for you.

Everything is Gaussian!
-----------------------

Of course not everything you're measuring is gaussian, but if you're measuring anything 
that isn't a kind of counting experiment, then the approximation is good enough most of the time. 

If you're building a nuclear power plant maybe don't listen to this advice. But often the 
question isn't whether to assume a Gaussian distribution or properly calculate the distribution, but 
make a simple error calculation or not produce uncertainties at all, so here we'll assume 
that everything we measure follows a gaussian distribution and that will lead to simple rules
that we can apply everywhere without adding much work to the process. 

It's a simple question of cost and benefit. So let's see what we can do. 

A simple experiment
-------------------

Back to our experimentation of adding feature X to our ficticious ML model.
To investigate if the new feature helps things we run the model twice, one with 
the feature enabled and once without. These are the results:

| Model | Without X | With X |
|-------|:---------:|:------:|
| Score |    2.9    |  3.2   |

Awesome. Our model improved by a whopping 0.3. Let's deploy the feature and call it a day. 
Not so fast! ML models are stochastic processes, that means if we train the model again
(especially with different data) we'll get different results. 

In production, we want to retrain the model every week and add the new data that came in 
so the best way to test the distribution the model performance will follow is cross validation
we train the model 5 times, each time with a different training set and evaluating against a different
test set. The output looks as follows:

| Model | Without X | With X |
|-------|:------:|:---------:|
| Score |  2.9   |    3.2    |
| Score |  3.0   |    2.8    |
| Score |  2.7   |    3.1    |
| Score |  2.9   |    2.8    |
| Score |  2.8   |    3.0    |

Suddenly the difference doesn't look as cotton dry anymore. Let's do the math. 
The thing that interests us now across all those experiments is how each model
performs on average, let's estimate the distribution by calculating the mean and standard deviation.

| Model | Without X | With X |
|-------|:------:|:---------:|
| Mean  |  2.86  |   2.98    |
| STD   |  0.10  |   0.16    |

The standard deviations tells us the width of the distribution of the individual measurements. 
so we could write that if we trained the model again with feature X, we would get 

$$ With X = 2.98 \pm 0.16 $$

This is already a good result because it tells us what performance to expect if we retrained
the model with new data. But we would like to compare the two models. For this it's best 
to look into which model performs better on average. For the moment you'll have to trust me, 
but the error on a mean value is equal to:

$$ \sigma_{mean(A)} = {\sigma_{A} \over \sqrt{N}}  $$

Where N is the number of experiments you did. \( \sigma \) is the sign for the error of something. 
By dividing the standard deviations above by \( \sqrt{5} \approx 2.24 \) we get 

| Model             | Without X | With X |
|-------------------|:---------:|:------:|
| Mean              |   2.86    |  2.98  |
| Error on the Mean |   0.05    |  0.07  |

The errors on the mean are smaller than the individual error. This makes sense because 
since we performed multiple experiments we know the average more accurately than where 
individual measurements might be. 

The second step is to compare how each model performs by calculating the difference. For this the rule is:

$$ \sigma_{A - B} = {\sqrt{ \sigma_{A}^2 + \sigma_{B}^2}}  $$

So the difference in mean is \( 2.86 - 2.98 = 0.12 \) and the error on  this difference is
\( {\sqrt{{0.05}^2 + {0.07}^2}} = 0.09 \). So our final measurement of the improvement
is:

$$ Improvement = 0.12 \pm 0.09 $$

From this we can tell that on average, a model with feature X will be between 0.03 and 0.21 better than a model without 
feature X in 68% of cases. (Because we used the standard deviation as a starting point which corresponds to a 68% Confidence Level)

If we want to know if this difference is significant with a 95% Confidence level you can simply check 
if this difference is more than "2\( \sigma \)" away from 0. 2\(\sigma\) is \(2 \cdot 0.9 = 0.18\) which is larger
than the 0.12 average difference. So the difference is **not** significant. There is a good chance 
that the difference we saw is in fact random noise. But since we now know much more than just 
the significance we are now in a better position to proceed. We can either drop the feature to avoid the risk of 
worsening the mode, add the feature because the chance of improvement is higher than the contrary or gather more data 
to obtain a smaller range. 

I hope the example already gave you a good picture of how to apply errors in your experiments, now the only thing 
missing is to show how the formulas above were obtained and how to deal with other operations than mean or sum.

Error Propagation
-----------------

Error propagation is the process of calculating the error on a variable that is calculated from a set of 
other variables with errors attached to them. Let's say we have a variable \(x\) with uncertainty \(\sigma_{x}\).
and we would like to calculate the uncertainty \(y=f(x)\). In principle what we would need to do is to apply the function
\(f\) to any value that x could take according to its distribution, see what distribution that would produce and then calculate 
the uncertainty from that. But we can simplify by assuming that f is close to linear in a small area around the mean value of x which we call \(\ \mu_x ). 
(First order Taylor expansion). The proof in 1 d goes as follows. 

\begin{equation}
\begin{split}
y = & f(x) \\ 
y \approx & f(\mu_x) + \frac{\partial f}{\partial x}\Big|_{x=\mu_x}(x-\mu_x) \\
y - f(\mu_x) \approx & \frac{\partial f}{\partial x}\Big|_{x=\mu_x}(x-\mu_x) \\
E[(y - f(\mu_x))^2] \approx & (\frac{\partial f}{\partial x}\Big|_{x=\mu_x})^2E[(x-\mu_x)^2] \\
\sigma_y = & \frac{\partial f}{\partial x} \Big|_{x=\mu_x} \sigma_x
\end{split}    
\end{equation}

If it's a bit much for you feel free to skip it, but in principle we just apply the linear approximation, 
then subtract \( f(\mu_x) \) on both sides, square and calculate the estimated value on both sides. Then we simply need to know
that \(  E[(y - f(\mu_x))^2] = \sigma_y\) is the definition of the variance and we obtain that we 
can calculate \( \sigma_y \) with the simple formula

$$ \sigma_y = \frac{\partial f}{\partial x} \Big|_{x=\mu_x} \sigma_x $$

A simple example of applying this formula is to calculate the error of \( y = x^2 \) the formula becomes

$$ \sigma_y = \frac{\partial f}{\partial x} \Big|_{x=\mu_x} \sigma_x = 2 \mu_x \sigma_x $$ 

If \( x = 2 \pm 1 \) then \( y = 4 \pm 4\). 

The formula can be easily expanded into multiple dimensions. The only difference is that we no longer can get 
rid of the squares in the end because of the sum. 

\begin{equation}
    \begin{split}
    y = & f(x_1, x_2, x_3, x_4, ...) \\
    \sigma_y^2 = & \sum_i (\frac{\partial f}{\partial x_i} \Big|_{x_i=\mu_{x_i}})^2  \sigma_{x_i}^2 \\
    \end{split} 
\end{equation}

Now finally we can obtain the formulas from the beginning. First, I'll only show the proof of the difference, 
but the one for the mean is equally simple. 

\begin{equation}
\begin{split}
    y & = x_1 - x_2 \\
    \Rightarrow \sigma_y^2 & = (\frac{\partial y}{\partial x_1})^2 \sigma_{x_1}^2 + (\frac{\partial y}{\partial x_2})^2 \sigma_{x_2}^2 \\
    & = \sigma_{x_1}^2 + \sigma_{x_2}^2 \\
    \Rightarrow \sigma_y & = \sqrt{\sigma_{x_1}^2 + \sigma_{x_2}^2} \\
\end{split}
\end{equation}

So now you should be able to propagate your uncertainties no matter which calculations you do with them.

The python uncertainties package
--------------------------------

If you're in python, you can avoid having to deal with all the math and simply use the [uncertainties](https://pythonhosted.org/uncertainties/) package. 
It's a pretty awesome piece of software which allows you to define variables with uncertainties. 

```python
>>> from uncertainties import ufloat
>>> x = ufloat(2, 1)
>>> print(x)
2.00+/-1
```
And the best thing about it is it can do the error propagation for you
```python
>>> x**2
4.00+/-4.0
```
Which is exactly what we calculated in the previous chapter. If you calculate the uncertainties of your experiments once 
and put them into a ufloat, then you can stop worrying about the uncertainties and treat them like normal numbers. 

Conclusion
----------

I hope I managed to give you a little bit of an introduction into uncertainties and gave you enough tools to get started. 
In short, the key points are:

1. Do any experiment multiple times and calculate the standard deviation. 
2. Add them to any result and plot you produce. Now any reader can estimate the uncertainty of your measurement. 
3. Use the ufloat package. It is awesome.
