
## Layer 2, Head 5 of: The stop sign was painted [MASK]. --> predictions: 1. red 2. white 3. black
### (There are many other layers/heads where a significant correlation between [MASK] and painted was found)

Analysis / observation:
The attention in layer 2, head 5 is focused on the connection between [MASK] and painted. In many other examples like this, the model used words surrounding [MASK] to infer that [MASK] could be a color. In this one, the model correlated paint with [MASK] to guess colors, most likely of which was red. This shows that the model is capable of making color inferences. 


Example Sentences:
- The [MASK] sky stretched above us. --> predictions: 1. night 2. blue 3. dark
- After it rained, the grass was bright [MASK]. --> predictions: 1. green 2. red 3. orange


## Layer 10, Head 7 of: As he was about to lose the race, he had to [MASK] to the end. --> predictions: 1. get 2. fight 3. race

Analysis / observation:
At first glance, layer 10, head 7 seems rather ordinary; however, when you really look closer into it, you can see how the AI considers context to. In the above sentence, we can tell that [MASK] is going to be a word like ran or sprint: not slowly walked. How do we know this, though? We know this because of the presence of the verb "lose". In layer 10, head 7 the connection between the words "lose" and "mask" is evident.  

Example Sentences:
- As the enemy closed in, they had to [MASK] for safety. --> Predictions: 1. run 2. flee 3. retreat ## This one has a very strong connection! Run, flee, retreat all seem based on the context of "enemy closed in".
- Hearing the final whistle, the team tried to [MASK] one last time. --> Predictions: 1. score 2. play 3. rally ## This one too shows that the model looks at context clues. 

