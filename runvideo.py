import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# YouTube API key - Replace with your own key
API_KEY = 'AIzaSyD6DZ-GlpIz7WH1u8vJiZK_NNCFoWR9cq4'

# YouTube Data API v3 service
youtube = build('youtube', 'v3', developerKey=API_KEY)


def search_videos(query, max_results=5):
    try:
        # Search for videos with the given query
        request = youtube.search().list(
            part='snippet',
            q=query,
            type='video',
            maxResults=max_results
        )
        response = request.execute()

        # Extract video details
        videos = []
        for item in response['items']:
            video = {
                'title': item['snippet']['title'],
                'video_id': item['id']['videoId'],
                'thumbnail': item['snippet']['thumbnails']['medium']['url']
            }
            videos.append(video)

        return videos

    except HttpError as e:
        st.error(f'An error occurred: {e}')


# Streamlit app
def main():
    st.title('Video Recommendation')
    st.write('Welcome! This will recommend motivational, relaxing, stress busters, and light comedy videos from YouTube.')

    # Predefined categories
    categories = {
        'Motivational': 'inspirational videos',
        'Relaxing': 'relaxation music',
        'Stress Busters': 'stress relief techniques',
        'Light Comedy': 'comedy skits'
    }

    # Recommendation selection
    selected_category = st.selectbox('Select a category', list(categories.keys()))

    # Show videos button
    if st.button('Show Videos'):
        # Search videos
        videos = search_videos(categories[selected_category])
        if videos:
            for video in videos:
                st.video(f'https://www.youtube.com/watch?v={video["video_id"]}')
        else:
            st.warning('No videos found.')


if __name__ == '__main__':
    # Set background image with CSS
    def add_bg_from_url():
        st.markdown(
            f"""
             <style>
             .stApp {{
                 background-image: url("https://i.pinimg.com/originals/24/cf/eb/24cfeb4cf8d60365f5f87ee7c09a1054.gif");
                 background-attachment: fixed;
                 background-size: cover
             }}
             </style>
             """,
            unsafe_allow_html=True
        )


    add_bg_from_url()

    main()
