3 Things Every Data Scientist Should Know
=======================================

Table of Contents
-----------------
[TOC]

Being a data scientist is hard. People expect you to do everything, and because the subject 
is much younger than other software related fields, the best practices aren't as well-developed yet. 
I thought it might be a good idea to write down 5 things I find key in doing good data science 
and that might help you on your journey.

1 Write down everything!
------------------------
Data Science is a game of knowledge. Every working day you gather more knowledge and add it to the pile. 

But if it is not documented, knowledge gets forgotten quickly and you're bound to repeat experiments again and again, 
because you don't know exactly what the result was last time. 

This can be done with an excel-sheet, confluence or even a piece of paper, but there exist experiment tracking tools 
like MLFlow or Tensorboard, where you set up that the parameters and results of your experiments are written 
to some central place, and you'll be able to look up past results easily. 

But this is not enough. Soon you'll have more experiments lying around than you can count, and you 
wouldn't be able to find anything, even if you tried. You have to clean up your space regularly and 
add descriptions and conclusions to your experiments. This way, it will feel like a library you can 
always come back to. 

2 Make experiments fast!
-------------------------
At the very start of a new project it makes sense to start working on some data in a 
notebook and see what you can do with it. But quickly you might notice that you have 12 notebooks lying around, 
all copying code from one another and each time you want to try something new, it takes ages because you need to 
find the code you need and stick it together like Frankensteins monster. 

At this point (or ideally before it comes this far) it makes sense to stop and consolidate your experiment setup. 
Write a python script that runs through your Analysis or Model Training start to finish and produces all relevant 
results. Push it to git-hub. Maybe even containerize it, so you can run many experiments at the same time.

Now your experimenting setup becomes:

1. Change 1 small detail in teh experiment
2. Run The experiment
3. Store Results

You see it has become really easy to run experiments, and since the results are standardized, it becomes really easy 
to compare runs. If it sounds too easy, it is.... but I myself fell down the trap of not doing this soon enough 
many times. 

3 Insights are products too!
-------------------------
I hear Data Science being conflated with "AI model building" way too often. It is not. Sometimes AI models are
a path towards what the company actually wants: **knowledge**, but very often it is also not.  

Sometimes a good visualization, a dashboard or a statistical analysis can provide way more value than 
your model, even if it worked the way you promised in the beginning. (Sorry)

Don't just assume the solution to every problem being a model. First try to learn as much about your 
data, try to gain insights. One sentence in a presentation could transform the whole business. 

If the knowledge the stakeholders are looking for is not as simple, maybe a dashboard on past data 
might help. Talk to your stakeholders often. They know much better than you what they need. 

Of course often you do end up needing some kind of model, but don't be the hammer that sees everything as a nail.




