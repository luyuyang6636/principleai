import os
from anthropic import Anthropic
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
api_key = os.environ.get("YOUTUBE_API_KEY")
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
client = Anthropic(api_key=anthropic_api_key)


# Send the formatted content to Claude for analysis

def create_summary():
    transcript = input("Enter a clean transcript: ")
    prompt = """Below the instruction is a transcript for a class in secondary school. Your goal is to summarise the transcript. This is how you should summarise the transcript: begin with a brief introduction that provides context about the subject of the lesson. First give definitions of key concepts/words in the class, then summarise the main topics and concepts covered in class. make sure to cover all key concepts in the transcript and do not miss any concepts.
    please only use the knowledge provided in the transcript and do not search for extra definition of the concepts elsewhere. the main points are the fundamental ideas that students should understand after attending the class. Make sure to highlight these points clearly. Structure the summary in a logical and organized manner. You can use bullet points and sub bullet points or numbered lists to separate different topics or concepts. Write the summary in clear and simple language that is easy for middle school students to understand. Avoid using jargon or complex terminology unless it's essential to the topic. If appropriate, include examples or illustrations to help clarify the main points. Wrap up the summary with a brief conclusion that reinforces the key takeaways from the lesson. 
    Here is an example of a good summary:
    Today's class focused on the process of <t_1>photosynthesis</t_1>, which is how plants convert sunlight into energy to fuel their growth and produce oxygen.
    Main Points:
    * Photosynthesis is a vital process for all living organisms because it produces oxygen and provides energy for plants.
    * The two main stages of photosynthesis are the <t_2>light-dependent reactions</t_2> and <t_3>the Calvin cycle</t_3>.
    * During the light-dependent reactions, sunlight is absorbed by <t_4>chlorophyll</t_4> in the <t_5>chloroplasts</t_5> of plant cells, which generates energy in the form of <t_6>ATP</t_6> and releases oxygen as a byproduct.
    * In the Calvin cycle, carbon dioxide is converted into <t_7>glucose</t_7> using the ATP produced during the light-dependent reactions.
    * Photosynthesis takes place in the chloroplasts of plant cells, primarily in the leaves.
    Can you also identify around 10 keywords and put it into numbered XML tag <terminology_#></terminology_#>. The keywords would be important concepts that are relevant to the main topic of class and could spark further research by the student similar to example above. 
    """
    content = f"{prompt} {transcript}"
    message = client.messages.create(
        max_tokens=3000,
        messages=[
            {"role": "user", "content": content},
        ],
        model="claude-2.1",
    )
    return message


def search_videos_by_keyword():
    keyword = input("Enter a keyword:")
    youtube = build("youtube", "v3", developerKey=api_key)

    # Call the search.list method to retrieve search results
    search_response = youtube.search().list(
        q=keyword,  # Keyword to search for
        part="snippet",
        type="video",
        maxResults=5  # Number of results to retrieve
    ).execute()

    # Extract video IDs and construct video links
    video_links = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            video_id = search_result["id"]["videoId"]
            video_link = f"https://www.youtube.com/watch?v={video_id}"
            video_links.append(video_link)
    best_video_link = best_video(video_links, keyword)

    return best_video_link

def best_video(video_links, keyword):
    best_video_link = None
    best_score = -1
    prompt = "Based on whatever information you are able to use at the youtube link provided after the scoring criterion. Output a score from 0 to 10, where 0 means the video is completely inappropriate or unrelated, and 10 means the video is perfectly suitable and highly relevant.” Try to not always rate the same thing. Please only output a number and nothing else. The factors to consider include: based on the keyword provided after this instruction and video link, does this video seem to provide accurate information about the keyword? Is the video created by credible and reputable sources (such as trusted experts and recognised educational institutions). Secondly, will this video likely provide clarity and improve students’ understanding on this keyword. Try to avoid videos that seem to use overly complex languages. Thirdly, does the video seem to be interesting to watch, does it seem to have engaging visuals, animations etc? Fourthly, take into account the length of the video, we do not want a video that is either too long and loses the student’s interest or too short to cover the topic adequately. Fifthly, is it likely that video will contain inappropriate content such as violence, pornography, and rude language? We want to avoid these videos at all costs. Lastly, check the reviews and ratings of the video as a reference to the quality of the video. "

    for video_link in video_links:
        video_id = video_link.split("=")[-1]
        youtube = build("youtube", "v3", developerKey=api_key)

        # Retrieve video statistics
        video_response = youtube.videos().list(
            part="statistics",
            id=video_id
        ).execute()

        view_count = int(video_response["items"][0]["statistics"]["viewCount"])
        content = f"{prompt}, {video_link}, {keyword}"

        message = client.messages.create(
            max_tokens=200,
            messages=[
                {"role": "user",
                 "content": content},
            ],
            model="claude-2.1",
        )

        print (message.content)

        try:
            score = float(message.content[0].text)
            # Calculate the final score based on the view count and Claude's assessment
            final_score = score * (1 + (view_count / 100000000))  # Adjust the weight given to view count as needed
            print(final_score)
            print(video_link)
            if final_score > best_score:
                best_score = final_score
                best_video_link = video_link
        except ValueError:
            print(f"Could not parse score from Claude's response for link: {video_link}")

    return best_video_link

def generate_definition(keyword):

  message = client.messages.create(
    max_tokens=100,
    messages=[
      {"role": "user", "content": f"Provide a short (3 - 4 sentences) definition for the term '{keyword}'. If possible, break down the etymology of the word into its component parts and explain the meaning of each part. Use a format like: WordPart: definition of this word part. Provide examples if helpful. Bear in mind that the aim of this is to help students aged (11 - 18) to better understand a kayword, so try to make the definition as easy to understand as possible. the structure of your answer should be you explain each word parts, seperated by new lines, then give a complete definition of the whole word. an example would bephotosynthesis -> Photo: This prefix comes from the Greek word 'phōs,' meaning 'light.' In the context of photosynthesis, 'photo' refers to light. Synthesis: This word comes from the Greek word 'synthesis,' which means 'putting together' or 'combining.' In the context of photosynthesis, 'synthesis' refers to the process of combining simple substances to form more complex ones. Putting it together, 'photosynthesis' literally means 'light synthesis' or 'putting together with light.'"
       }
    ],
    model="claude-2.1",
  )

  response = message.content[0].text

  return response

print(generate_definition("capitalism"))

#print(create_summary())
