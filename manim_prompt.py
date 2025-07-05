def m_prompt(visuals,text):
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