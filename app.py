import streamlit as st
import os
import datetime

css = """
<style>
    @media only screen and (max-width: 600px) {
        .app-description {
            font-size: 18px;
            animation: fadeIn 2s;
        }
    }

    @keyframes fadeIn {
        0% {
            opacity: 0;
        }
        100% {
            opacity: 1;
        }
    }
</style>
"""

# Display CSS
st.write(css, unsafe_allow_html=True)

# Describe the app with Markdown and CSS
st.markdown("<div class='app-description'><h1><marquee>🤖🤖🤖  🙏🙏  💚  Welcome to DDU-BLOG-APP  🤖🤖🤖 🙏🙏   ❤️                   </marquee></h1></div>", unsafe_allow_html=True)
st.markdown("<div class='app-description'><h1><marquee>🤖🤖Where Create Posts by upload image, video, audio🤖🤖</marquee></h1></div>", unsafe_allow_html=True)

# Set up a directory for saving the blog posts, images, audio, and video files
if not os.path.exists("blog_posts"):
    os.makedirs("blog_posts")
if not os.path.exists("blog_images"):
    os.makedirs("blog_images")
if not os.path.exists("blog_audio"):
    os.makedirs("blog_audio")
if not os.path.exists("blog_video"):
    os.makedirs("blog_video")

# Password for blog deletion (change this to your desired password)
DELETE_PASSWORD = "Vinay@123"

# Define the sidebar for creating new blog posts and deleting existing ones
def create_sidebar():
    st.sidebar.title("Blog Actions")
    action = st.sidebar.radio("Select Action", ("Create New Post", "Delete Post(by developer)", "Search by Tags"))

    if action == "Create New Post":
        create_new_post()
    elif action == "Delete Post(by developer)":
        delete_post()
    elif action == "Search by Tags":
        search_by_tags()


# Function to create a new blog post
def create_new_post():
    st.sidebar.title("Create New Blog Post")
    post_title = st.sidebar.text_input("Title")
    post_tags = st.sidebar.text_input("Tags (comma-separated)")
    post_content = st.sidebar.text_area("Content", height=500)
    post_formatting = st.sidebar.selectbox("Formatting", ["Markdown", "Plain Text"])
    post_image = st.sidebar.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])
    post_audio = st.sidebar.file_uploader("Upload an audio file (optional)", type=["mp3", "wav"])
    post_video = st.sidebar.file_uploader("Upload a video file (optional)", type=["mp4", "avi", "mov", "mkv"])
    post_url = st.sidebar.text_input("Embed URL (optional)")

    if st.sidebar.button("Create"):
        # Save the blog post and any uploaded files
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        post_filename = f"{timestamp}-{post_title}.md"
        with open(f"blog_posts/{post_filename}", "w") as f:
            f.write(f"Title: {post_title}\n")
            f.write(f"Tags: {post_tags}\n")
            f.write(f"Timestamp: {timestamp}\n")
            if post_image is not None:
                image_filename = f"{timestamp}-{post_image.name}"
                with open(f"blog_images/{image_filename}", "wb") as img_file:
                    img_file.write(post_image.getbuffer())
                f.write(f"Image: {image_filename}\n")
            if post_audio is not None:
                audio_filename = f"{timestamp}-{post_audio.name}"
                with open(f"blog_audio/{audio_filename}", "wb") as audio_file:
                    audio_file.write(post_audio.getbuffer())
                f.write(f"Audio: {audio_filename}\n")
            if post_video is not None:
                video_filename = f"{timestamp}-{post_video.name}"
                with open(f"blog_video/{video_filename}", "wb") as video_file:
                    video_file.write(post_video.getbuffer())
                f.write(f"Video: {video_filename}\n")
            if post_url:
                f.write(f"URL: {post_url}\n")
            f.write("\n")
            f.write(post_content)
        st.sidebar.success("Blog post created!")


# Function to delete an existing blog post
def delete_post():
    st.sidebar.title("Delete Blog Post(by developer)")
    delete_password = st.sidebar.text_input("Delete Password", type="password")
    if delete_password == DELETE_PASSWORD:
        post_files = os.listdir("blog_posts")
        if not post_files:
            st.info("No blog posts to delete.")
        else:
            post_to_delete = st.sidebar.selectbox("Select Post to Delete", post_files)
            if st.sidebar.button("Delete"):
                os.remove(f"blog_posts/{post_to_delete}")
                st.sidebar.success(f"Blog post '{post_to_delete}' deleted successfully.")
    elif delete_password:
        st.sidebar.error("Incorrect delete password.")


# Function to search blog posts by tags
def search_by_tags():
    st.sidebar.title("Search by Tags")
    search_tags = st.sidebar.text_input("Enter Tags (comma-separated)")
    search_tags = [tag.strip() for tag in search_tags.split(",") if tag.strip()]
    if st.sidebar.button("Search"):
        post_files = os.listdir("blog_posts")
        found_posts = []
        for post_file in post_files:
            with open(f"blog_posts/{post_file}", "r") as f:
                post_content = f.read()
                post_lines = post_content.split("\n")
                post_tags = post_lines[1][6:].split(",")
                if all(tag in post_tags for tag in search_tags):
                    found_posts.append(post_content)
        if found_posts:
            for post_content in found_posts:
                st.write(post_content)
        else:
            st.info("No posts found with the provided tags.")


# Define the main content area for viewing existing blog posts
def create_main_content():
    page_icon = ":enginer:"
    st.title("DDU-BLOG-APP")
    st.subheader('[Developed by Vinay](https://github.com/vinne01)')

    post_files = os.listdir("blog_posts")
    if not post_files:
        st.info("No blog posts yet.")
    for post_file in post_files:
        with open(f"blog_posts/{post_file}", "r") as f:
            post_content = f.read()
            post_lines = post_content.split("\n")
            post_title = post_lines[0][7:]
            post_tags = post_lines[1][6:].split(",")
            post_timestamp = post_lines[2][11:]
            post_image = None
            post_audio = None
            post_video = None
            post_url = None
            for line in post_lines[3:]:
                if line.startswith("Image: "):
                    post_image = line[7:]
                elif line.startswith("Audio: "):
                    post_audio = line[7:]
                elif line.startswith("Video: "):
                    post_video = line[7:]
                elif line.startswith("URL: "):
                    post_url = line[5:]
            post_content = "\n".join(post_lines[3:])
            st.write(f"## {post_title}")
            st.write(f"*Tags:* {' '.join(['`' + tag.strip() + '`' for tag in post_tags])}")
            st.write(f"*Date/Time:* {post_timestamp}")
            if post_image is not None:
                st.image(f"blog_images/{post_image}", use_column_width=True)
            if post_audio is not None:
                st.audio(f"blog_audio/{post_audio}", format='audio/wav')  # Change format as per your audio file
            if post_video is not None:
                st.video(f"blog_video/{post_video}")  # Streamlit automatically detects video format
            if post_url:
                st.write(f"[Link]({post_url})")
            if post_file.endswith(".md"):
                st.markdown(post_content)
            else:
                st.write(post_content)


# Run the app
create_sidebar()
create_main_content()
