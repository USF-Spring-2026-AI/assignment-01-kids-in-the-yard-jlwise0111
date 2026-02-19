# AI Assignment 01 - Kids in the Yard

Comparison
* Which tool(s) did you use?/If you used an LLM, what was your prompt to the LLM? 
  * I used ChatGPT. My prompt was an edited down version of the instructions to create a family tree simulation begining with two people born in 1950 and generating children/descendents until 2120. I included the design suggestions provided to us in the instructions. I also included that there would need to be the three features for interacting with the tree.  
* What differences are there between your implementation and the LLM? 
  * The LLM implementation had recursion in FamilyTree so PersonFactory only created single individuals. I kept recursion in PersonFactory, created the first couple in FamilyTree and then called create_children to begin the recursion in PersonFactory.
* What changes would you make to your implementation in general based on suggestions from the
LLM? 
  * One difference/suggestion I found interesting was separating partner relationships from parent/child relationships, This would help simplify traversal. One implementation I made with the help of the LLM was the pretty_print function. Given that this was not part of the project requirements, I thought it seemed acceptable to use AI assistance for. I was mainly interested in seeing the full tree built out.
* What changes would you refuse to make?
  * As I said above, the LLM had recursion in FamilyTree. Although this may make stopping conditions easier to enforce, I already have a working program and do not want to change it and risk breaking other parts.
