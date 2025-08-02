def ask_for_story(input_prompt):
    return f'strictly answer to this query in a way that youtube video can be created using it: {input_prompt}'

def dialogue_prompt(Story):
    prompt='''Your task is to convert narrative input into timed 5-15 second multimedia segments(Strictly each segment should have its own independent meaning,so that if  segment is missing it should not effect the whole video)..Most important and strictly All dialogues should be carry meaning together as well as alone. For each segment provide:
    
   
    Visual description: Manim-compatible scene description , example:("frog jumping in 8X8 matrix diagonally from 0,0 to 7,7, use dark 
    and light grey for grid colors with white lines for grid structure and use black background, frog should be green with white eye and frog structure " ),("create isaac newton seating under tree , draw its actual face and apple should fall on him , make it funny"),  Be as sepecific as possible, mention eye smoothing and realistic, You can use any symbol here or numbers or anything needed

    Speech text:  Strictly contains words to be spoken only in lower case latin letters words and punctuations where needed (use it one at a time),(if you want to use numbers or mathematical operation use words only example five plus two equals seven,use phi or theta etc for their symbols etc ),strictly no symbols or special characters, also text like umm , meow etc. are allowed too, Short form must be sperated by space example :(use "U P I" instead of "UPI", execption": for "AI" use "AI" only)
   
    **use proper breaks in Speech**
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

# TODO: changed
def manim_code_prompt(visuals,text,error=''):
    prompt='''You are working in backend system of a video editing tool. Your task is to generate Manim code( version Manim Community v0.19.0) for a given set of visuals and text.
    Generate Manim code as simple text with proper indentations adhering to:  
     **visuals should make sense with context and should be apealing,use good colours and diagram**
    **text should be clear and easy to read**
    **text or structures should not overlap**
    **Strictly do not write subtitle in the video**
    -strictly do not use unscesary text in video
    -strictly do not use unscesary text in video
    -strictly do not use unscesary text in video
    -strictly do not use unscesary text in video
    -strictly do not use unscesary text in video
    **First decide which Manim Objects you need. Then write each call in order. Finally, combine them in a Group if needed.**
    1. **Mandatory Structure**  
    - Class name: `class Frame(Scene):`  
    - Strictly Do not create  or use any files
    -strictly Do not use or create any audio files
    -Strictly do  not use any image in the code 
    -Strictly do not write text explaining the visuals
    Strictly use dimensions 1920x1080
    Strictly use dimensions 1920x1080   
    Strictly use dimensions 1920x1080
    Strictly use dimensions 1920x1080
    **strictly do not make any run time errors**
    2. **Visual Requirements**  
    {''' + visuals + '''}  
    Donot just add Visuals as text , it should be drawn in the video
    - context for the visuals: {'''+text+ '''}
    - Allow elements ONLY if they:  
        a) Strictly Don't overlap  content  
        b) Strictly Don't exceed  frame space 
        c) Strictly Don't distract from primary content
        d) Strictly Remove elements that isn't necessary further 
        e) Strictly Do not end animation with black screen(without any content)
        f) Strictly Do not use any external libraries other than manim
        g) Strictly Try to keep content in center(without overlapping)
    **Strictly do not write subtitle in the video**
    **Strictly do not write subtitle in the video**
    **Strictly do not write subtitle in the video**
    **Strictly do not write subtitle in the video**
    **Strictly do not write subtitle in the video**
    Strictly use dimensions 1920x1080
    Strictly use dimensions 1920x1080   
    Strictly use dimensions 1920x1080
    Strictly use dimensions 1920x1080
    3. **Hard Constraints**  
    - Zero overlap of visuals
    - Zero overlap of text   
    - Single video output 
    _ Strictly use hex color codes for colors 

    -strictly do not use unscesary text in video
    4. **Output Rules**   
    - No markdown/comments/backticks 
    - strictly just return the code as string 
    -code should not contain infinte loops

    Strictly do not use any class you haven't defined example , "Tree" Or "CENTER"(Strictly Do not use it), Strictly write the code component that  you was to use do not pre assume any codebase,focus on  Manim Community v0.19.0 then write code
    Make it visually appealing and engaging.
    Strictly do not fade that's not have been created in codes.
    Check thoroughly everything works correctly with  Manim Community v0.19.0.
    Make  it natural 
    
    **MAKE SMART USE OF SHAPES AND COLOURS**
    **MAKE changes if needed (without changing the context)**
    **use eye smoothing colours**
    Example response:  
     "from manim import *\nclass Frame(Scene):\n    def construct(self):\n        sky = Rectangle(width=self.camera.frame_width, height=self.camera.frame_height, fill_color="#87CEEB", fill_opacity=1).move_to(ORIGIN)\n        sun = Circle(radius=1.0, fill_color="#FFD700", fill_opacity=1).to_corner(UR).shift(LEFT * 0.5 + DOWN * 0.5)\n        cloud1 = VGroup(Circle(radius=0.5, fill_color=WHITE, fill_opacity=1).shift(UP * 3 + LEFT * 2), Circle(radius=0.4, fill_color=WHITE, fill_opacity=1).shift(UP * 3.2 + LEFT * 1.5), Circle(radius=0.45, fill_color=WHITE, fill_opacity=1).shift(UP * 3.1 + LEFT * 2.5))\n        cloud2 = VGroup(Circle(radius=0.4, fill_color=WHITE, fill_opacity=1).shift(UP * 2.5 + RIGHT * 1), Circle(radius=0.35, fill_color=WHITE, fill_opacity=1).shift(UP * 2.7 + RIGHT * 1.5), Circle(radius=0.45, fill_color=WHITE, fill_opacity=1).shift(UP * 2.6 + RIGHT * 0.5))\n        ground = Rectangle(width=self.camera.frame_width, height=1, fill_color="#228B22", fill_opacity=1).to_edge(DOWN)\n        grass_blades = VGroup(*[Triangle(fill_color="#32CD32", fill_opacity=1, stroke_width=0).scale(0.2).next_to(ground.get_top() + DOWN * 0.05, RIGHT, buff=0.3 * i) for i in range(-10, 11)])\n        trunk = Rectangle(width=0.4, height=3, fill_color="#8B4513", fill_opacity=1).next_to(ground, UP, buff=0)\n        foliage = VGroup(Circle(radius=1.5, fill_color="#006400", fill_opacity=1).shift(trunk.get_top() + UP * 0.5 + LEFT * 0.3), Circle(radius=1.2, fill_color="#2E8B57", fill_opacity=1).shift(trunk.get_top() + UP * 0.6 + RIGHT * 0.5), Circle(radius=1.3, fill_color="#228B22", fill_opacity=1).shift(trunk.get_top() + UP * 0.8 + LEFT * 0.5))\n        head = Ellipse(width=0.8, height=1.2, fill_color="#FFE5B4", fill_opacity=1).move_to([0, ground.get_top()[1] + 1.2, 0])\n        wig_cap = Ellipse(width=1.2, height=0.6, fill_color=WHITE, fill_opacity=1).move_to(head.get_top() + DOWN * 0.1)\n        curl1 = Arc(radius=0.5, start_angle=PI*1.1, angle=PI*0.8, color=WHITE, stroke_width=10).move_to(head.get_left() + UP*0.1)\n        curl2 = Arc(radius=0.5, start_angle=PI*0.2, angle=PI*0.8, color=WHITE, stroke_width=10).move_to(head.get_right() + UP*0.1)\n        left_eye = Dot(radius=0.05, color=BLACK).move_to(head.get_center() + LEFT * 0.15 + UP * 0.1)\n        right_eye = Dot(radius=0.05, color=BLACK).move_to(head.get_center() + RIGHT * 0.15 + UP * 0.1)\n        specs = VGroup(Circle(radius=0.1).move_to(left_eye.get_center()), Circle(radius=0.1).move_to(right_eye.get_center()), Line(left_eye.get_center() + RIGHT*0.1, right_eye.get_center() + LEFT*0.1, stroke_width=2))\n        mouth = Line(LEFT*0.1, RIGHT*0.1, color=BLACK).move_to(head.get_center() + DOWN * 0.1)\n        torso = Rectangle(width=0.8, height=1.2, fill_color="#4B0082", fill_opacity=1).next_to(head, DOWN, buff=0)\n        left_leg = Line(start=torso.get_bottom() + LEFT*0.2, end=torso.get_bottom() + LEFT*0.2 + DOWN*0.6 + RIGHT*0.2, stroke_width=6, color="#4B0082")\n        right_leg = Line(start=torso.get_bottom() + RIGHT*0.2, end=torso.get_bottom() + RIGHT*0.2 + DOWN*0.6 + LEFT*0.2, stroke_width=6, color="#4B0082")\n        newton = VGroup(head, wig_cap, curl1, curl2, left_eye, right_eye, specs, mouth, torso, left_leg, right_leg)\n        apple = Circle(radius=0.15, fill_color=RED, fill_opacity=1).move_to([0, foliage[0].get_center()[1], 0])\n        self.play(FadeIn(sky), FadeIn(sun), FadeIn(cloud1), FadeIn(cloud2))\n        self.play(FadeIn(ground), FadeIn(grass_blades))\n        self.play(FadeIn(trunk), FadeIn(foliage))\n        self.play(FadeIn(newton), FadeIn(apple))\n        self.wait(0.5)\n        self.play(apple.animate.move_to([0, head.get_center()[1] + 0.6, 0]), run_time=1)\n        self.play(Rotate(newton, angle=PI/12, about_point=head.get_center()), run_time=0.5)\n        self.play(Rotate(newton, angle=-PI/12, about_point=head.get_center()), run_time=0.5)\n        self.wait(1)
"

    '''
    return prompt

def svg_prompt(visuals, text):
    prompt='''You are working in backend system of a video editing tool. Your task is to generate svg code static one without animation just a single frame for a given set of visuals and text.
    Generate svg code as simple text with proper indentations adhering to:  
     **visuals should make sense with context and should be apealing,use good colours and diagram**
    **text should be clear and easy to read**
    **text or structures should not overlap**
    Stricly use dimensions 1920x1080
    Stricly use dimensions 1920x1080
    Stricly use dimensions 1920x1080
    **Strictly do not write subtitle in the video**
    **First decide which svg Objects you need. Then write each call in order. Finally, combine them in a Group if needed.**
    1. **Mandatory Structure**    
    -Strictly do  not use any external image in the code until mentioned
    -Strictly do not write text explaining the visuals
    2. **Visual Requirements**  
    {''' + visuals + '''}  
    - context for the visuals: {'''+text+ '''}
    - Allow elements ONLY if they:  
        a) Strictly Don't overlap  content  
        b) Strictly Don't exceed  frame space 
        c) Strictly Don't distrafct from primary content
        d) Strictly Remove elements that isn't necessary further 
        e) Strictly Do not end animation with black screen(without any content)
        f) Strictly Do not use any external libraries other than svg
        g) Strictly Try to keep content in center(without overlapping)
    3. **Hard Constraints**  
    - Zero overlap of visuals
    - Zero overlap of text   
    - Single image output 
    _ Strictly use hex color codes for colors 

    4. **Output Rules**   
    - No markdown/comments/backticks 
    - strictly just return the code as string 
    -code should not contain infinte loops
    Stricly use dimensions 1920x1080
    Stricly use dimensions 1920x1080
    Make it visually appealing and engaging.
    Strictly do not fade that's not have been created in codes.
    Check thoroughly everything works correctly with  svg 
    Make  it natural 
    
    **MAKE SMART USE OF SHAPES AND COLOURS**
    **MAKE changes if needed (without changing the context)**
    **use eye smoothing colours**
    Example response :  
    
    <svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
    <rect width="1920" height="1080" fill="#f0f8ff"/>
    <text x="960" y="540" font-size="120" text-anchor="middle" dominant-baseline="middle" fill="#333366" font-family="Arial">Hello</text>
    </svg>
    
    

    '''
    return prompt

def debug_prompt(code, error):
    prompt = f"""
You are tasked with debugging the following code.

Strict rules:
- Only debug the code; do not rewrite or reimagine it.
- Do not change the context or logic of the code.
- Do not alter variable names, function names, or class names.
- Only use the 'manim' library; no additional external libraries are allowed.
- Return the complete corrected code as **plain text** (without explaining about escaping characters like "\\" for JSON).

Here is the code:
{code}

Here is the error:
{error}

Format your final output strictly like this example:
"from manim import *\nclass Frame(Scene):\n    def construct(self):\n        text = Text('Hello').to_edge(CENTER, color='#FFFFFF')\n        self.play(Write(text))"
"""
    return prompt