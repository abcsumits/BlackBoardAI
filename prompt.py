def dialogue_prompt(Story):
    prompt='''Your task is to convert narrative input into timed 5-15 second multimedia segments(Strictly each segment should have its own independent meaning,so that if  segment is missing it should not effect the whole video)..Most important and strictly All dialogues should be carry meaning together as well as alone. For each segment provide:
    
   
     
    Visual description: Manim-compatible scene description (geometric primitives, mobjects, animations)(No constraints on visual description use whatever suits fine for the story)

    Speech text:  Strictly contains words to be spoken only in lower case latin letters words and "," or "." or "?",(if you want to use numbers or mathematical operation use words only example five plus two equals seven,use phi or theta etc for their symbols etc ),strictly no symbols or special characters

    Format strictly as plain-text JSON:
    {"segment1": ["visual description", "speech text"], "segment2": ["...", "..."], ...}

    Requirements:

    Use ONLY segment1, segment2 sequential numbering

    Visuals must use explicit Manim elements:
    ✓ Parametric shapes (Polygon, Arrow, Dot)
    ✓ Mathematical surfaces (Surface, 3DAxes)
    ✓ Color codes (HEX/RGB)
    ✓ Transform animations (Create, FadeIn, Rotate)
    ✓ No mention about commands or actions just the text that is to be spoken
    ✓ No mention of the audio or the flow
    Striclty do not add any code in visuals or audio(you can ignore that part of story)

    Speech text requirements:
    ✓ No contractions ("do not" not "don't")
    ✓ Max 1 comma per sentence
    ✓ Oxford comma usage
    ✓ Terminal punctuation only (.?!)
    ✓ No mention about commands or actions just the text that is to be spoken
    ✓ No mention of the visuals or the flow

    JSON must be:
    ✓ Wrapped in {} with double-quoted strings
    ✓ Proper comma placement
    ✓ No trailing commas
    ✓ Escape characters as \" if needed

    Example:
    {"segment1": ["A blue RegularPolygon(5) rotates clockwise on an orange background", "The ancient symbol begins to glow with pentagonal symmetry."]}

    Input Story:
    {'''+Story+'''}'''
    return prompt

def manim_code_prompt(visuals,text,error=''):
    prompt='''You are working in backend system of a video editing tool. Your task is to generate Manim code( version Manim Community v0.19.0) for a given set of visuals and text.
    Generate Manim code as simple text with proper indentations adhering to:  
    1. **Mandatory Structure**  
    - Class name: `class Frame(Scene):`  
    - Strictly Do not create  or use any files
    -strictly Do not use or create any audio files
    -Strictly do  not use any image in the code 

    2. **Visual Requirements**  
    {''' + visuals + '''}  
    - context for the visuals: {'''+text+ '''}
    - Allow elements ONLY if they:  
        a) Strictly Don't overlap  content  
        b) Strictly Don't exceed  frame space 
        c) Strictly Don't distract from primary content
        d) Strictly Remove elements that isn't necessary further 
        e) Strictly Do not end animation with black screen(without any content)
        f) Strictly Do not use any external libraries other than manim
        g) Strictly Try to keep content in center(without overlapping)
    3. **Hard Constraints**  
    - Zero overlap of visuals
    - Zero overlap of text   
    - Single video output 
    _ Strictly use hex color codes for colors 

    4. **Output Rules**   
    - No markdown/comments/backticks 
    - strictly just return the code as string 
    -code should not contain infinte loops

    Strictly do not use any class you haven't defined example , "Tree" Or "CENTER"(Strictly Do not use it), Strictly write the code component that  you was to use do not pre assume any codebase,focus on  Manim Community v0.19.0 then write code
    Make it visually appealing and engaging.
    Strictly do not fade that's not have been created in codes.
    Check thoroughly everything works correctly with  Manim Community v0.19.0.
    Make  it natural 
    Example response for "Hello":  
    "from manim import *\nclass  Frame(Scene):\n    def construct(self):\n       text = Text('Hello').to_edge(CENTER)\n      self.play(Write(text))"}  

    '''+error+'''
    '''
    return prompt