# Searchify
A personal project that I made to convert a script which grabbed basic information from a spotify playlist into a more expansive website which incorporated support for albums, individual tracks, playlists, artists, and the current user through the authorization flow. This was made with the Flask framework, as well as HTML, bootstrap CSS with PurgeCSS to reduce the size, and vanilla javascript.

After uploading as an all-in one Flask front-end and Flask back-end, I will transition to turning the flask portion into a restful API, and learn a framework and use the API to serve a new independent front end. Another potential goal regarding this could be integrating a database which I had in earlier commits but did not see the point for this particular project, as well as potentially using a CSS framework/preprocessor like Sass or tailwind.

## How to Use
You will need Python 3.

### 1. Clone or install repository
Clone the repository using git using
```in terminal bash
git clone https://github.com/wesngu28/spotifyapp.git
```
or click the green code button, download the zip and extract it.

### 2. Install Dependencies
In the terminal, use pip
```
pip install -r requirements.txt
```

### 3. Setup Spotify Developer
Open the [Spotify developer dashboard](https://developer.spotify.com/dashboard/). When there, you should see a client ID on the right. Copy the client ID into the config.py file over the placeholder string (removing the quotes). Click show client secret and do the same for the client secret.

Now, click on the green edit settings button on the left. Set your redirect URI to match config.
```
http://127.0.0.1:5000/callback/
```

If you would rather use a different port, you can define it yourself and change the value in config.py and make sure the redirect uri matches to callback properly during OAuth flow.

### 4. Run the Flask App
In the terminal, run
```
python searchify.py
```
Make sure to login with Spotify.
