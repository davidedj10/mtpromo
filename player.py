import vlc

# List of videos to play
videos = ["video1.mp4", "video2.mp4", "video3.mp4"]

# Create VLC instance
instance = vlc.Instance()

# Create a MediaPlayer object
player = instance.media_player_new()

while True:
    for video in videos:
        # Set the media to play
        media = instance.media_new(video)
        player.set_media(media)

        # Play the video
        player.play()

        # Wait for the video to finish
        while True:
            if player.get_state() == vlc.State.Ended:
                break
