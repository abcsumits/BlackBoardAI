def svg_prompt(visuals,text,dimension="1920x1080",image={}):
    prompt='''You are working in backend system of a video editing tool. Your task is to generate svg code static one without animation just a single frame for a given set of visuals and text.
    Generate svg code as simple text with proper indentations adhering to:  
     **visuals should make sense with context and should be apealing,use good colours and diagram**
    **text should be clear and easy to read**
    **text or structures should not overlap**
    Stricly use dimensions '''+dimension+'''
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

    Make it visually appealing and engaging.
    Strictly do not fade that's not have been created in codes.
    Check thoroughly everything works correctly with  svg 
    Make  it natural 
    
    **MAKE SMART USE OF SHAPES AND COLOURS**
    **MAKE changes if needed (without changing the context)**
    **use eye smoothing colours**
    Example response :  (here input dimension was 1920 x 1080)
    
    <svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
    <rect width="1920" height="1080" fill="#f0f8ff"/>
    <text x="960" y="540" font-size="120" text-anchor="middle" dominant-baseline="middle" fill="#333366" font-family="Arial">Hello</text>
    </svg>
    
    

    '''
    if image:
        for key in image:
            prompt+='\n    - Use the image provided for '+key+' in visuals , the description for this image is : '+image[key] + ". Make sure to integrate it well with the rest of the content."
    return prompt