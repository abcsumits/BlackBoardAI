from openAIapi import openapi
def title(story):
    return openapi('''You are agent , strictly just return the text(without any explantion), strictly follow youtubes guidelines for title,strictly dont use "<" or ">" in output,as youtube restricts this symbol in title,
                   strictly length of output string should be less than 50 characters
             for a youtube videos title that optimizes SEO and should be small(under the allowed length of video title ) for this story :'''+story)
def description(story):
    return openapi('''You are youtube description writer(without title) agent ,strictly dont use "<" or ">" in output,as youtube restricts this symbol in description, strictly just return the text(without any explantion),Strictly description should comply with youtube guidelines,
             strictly dont use any special characters in output(hashtags '#' are allowed),strictly dont use any emojis in output,strictly dont use any links in output,strictly dont use any code in output,strictly dont use any html tags in output,
                               strictly length of output string should be less than 10000 characters and use hashtags
             for Write a youtube videos description that optimizes SEO for this story :'''+story)
    