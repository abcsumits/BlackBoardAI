def d_prompt(Story):
    prompt='''Your task is to convert narrative input into timed 5-15 second multimedia segments(Strictly each segment should have its own independent meaning,so that if  segment is missing it should not effect the whole video)..Most important and strictly All dialogues should be carry meaning together as well as alone. For each segment provide:
    
   
     
    Visual description: Manim-compatible scene description , example:("frog jumping in 8X8 matrix diagonally from 0,0 to 7,7, use dark and light grey for grid colors with white lines for grid structure and use black background, frog should be green with white eye and frog structure " ),("create isaac newton seating under tree , draw its actual face and apple should fall on him , make it funny"),  Be as sepecific as possible, mention eye smoothing and realistic

    Speech text:  Strictly contains words to be spoken only in lower case latin letters words and punctuations where needed (use it one at a time),(if you want to use numbers or mathematical operation use words only example five plus two equals seven,use phi or theta etc for their symbols etc ),strictly no symbols or special characters, also text like umm , meow etc. are allowed too, Short form must be sperated by space example :(use "U P I" instead of "UPI", execption": for "AI" use "AI" only)
   
    **use proper breaks in Speech**
    Format strictly as plain-text JSON:
    {"segment1": ["visual description", "speech text"], "segment2": ["...", "..."], ...}

    **Visual description do not have any description, do not use any rules of speech on visuals**
    **use as many objects and scenes description as possible it should be visually appealing the visual will be directly passed to manim writer agent to convert it into video**
    Requirements:

    Use ONLY segment1, segment2 sequential numberings

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
