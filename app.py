import streamlit as st
import requests
import pandas as pd
from src.pipeline.predict_pipeline import PredictPipeline
from src.utils import load_object

API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# ========== SESSION STATE ==========
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'history' not in st.session_state:
    st.session_state.history = []
if 'trailer_url' not in st.session_state:
    st.session_state.trailer_url = None
if 'trailer_title' not in st.session_state:
    st.session_state.trailer_title = None
if 'show_recommendations' not in st.session_state:
    st.session_state.show_recommendations = False
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None

# ========== CSS ==========
st.markdown("""
<style>
    .stApp { background-color:#141414; color:white; }
    .stButton > button {
        background: linear-gradient(135deg, #e50914 0%, #b20710 100%);
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 5px;
        font-size: 12px;
        margin: 2px;
    }
    .stButton > button:hover { transform: scale(1.02); }
    img { border-radius: 8px; }
    .trailer-container {
        background: #1a1a1a;
        border-radius: 10px;
        padding: 15px;
        margin: 20px 0;
        border-left: 4px solid #e50914;
    }
    
    .favorite-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 10px;
        padding: 8px 12px;
        margin: 5px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.3s;
        border: 1px solid #2a2a3e;
    }
    .favorite-card:hover {
        transform: translateX(5px);
        border-color: #e50914;
    }
    .favorite-title {
        font-size: 14px;
        font-weight: 500;
        color: white;
    }
    .favorite-emoji {
        font-size: 16px;
        margin-right: 10px;
    }
    .favorite-count {
        background: #e50914;
        color: white;
        border-radius: 20px;
        padding: 2px 8px;
        font-size: 11px;
        font-weight: bold;
    }
    .history-card {
        background: #1f1f1f;
        border-radius: 8px;
        padding: 8px 12px;
        margin: 4px 0;
        font-size: 13px;
        color: #ddd;
        transition: all 0.2s;
        border-left: 3px solid #e50914;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .history-card:hover {
        background: #2a2a2a;
        color: white;
        transform: translateX(3px);
    }
    .history-title {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
    }
    .clear-btn {
        background: #333 !important;
        color: #ff6b6b !important;
        font-size: 11px !important;
        padding: 4px 10px !important;
    }
    .clear-btn:hover {
        background: #e50914 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommendation System")

# ========== LOAD MOVIES ==========
movies = load_object("artifacts/movies.pkl")
movie_list = movies["title"].values

# ========== EK HI BOX - SEARCH + SELECT ==========
st.markdown("### 🔍 Search a Movie")

# Selectbox with search functionality - yehi hai ek box
selected_movie = st.selectbox(
    "Type or select a movie",
    options=movie_list,
    index=None,
    placeholder="Search for a movie... (e.g., Avatar, Titanic)",
    key="movie_selector"
)

# Update selected movie
if selected_movie:
    st.session_state.selected_movie = selected_movie

# ========== FUNCTIONS ==========
def get_trailer_key(movie_name):
    try:
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
        search_data = requests.get(search_url).json()
        if search_data.get("results"):
            movie_id = search_data["results"][0]["id"]
            trailer_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"
            trailer_data = requests.get(trailer_url).json()
            for video in trailer_data.get("results", []):
                if video["type"] == "Trailer" and video["site"] == "YouTube":
                    return video["key"]
        return None
    except:
        return None

def get_movie_details(movie_name):
    try:
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
        data = requests.get(search_url).json()
        if data.get("results"):
            movie = data["results"][0]
            movie_id = movie["id"]
            details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
            details = requests.get(details_url).json()
            return {
                "id": movie_id,
                "title": movie["title"],
                "rating": round(movie.get("vote_average", 0), 1),
                "popularity": round(movie.get("popularity", 0), 1),
                "release_date": movie.get("release_date", "N/A")[:4],
                "runtime": details.get("runtime", "N/A"),
                "poster": f"https://image.tmdb.org/t/p/w200{movie['poster_path']}" if movie.get("poster_path") else None,
                "overview": movie.get("overview", "No overview"),
                "genres": [g["name"] for g in details.get("genres", [])],
                "language": details.get("original_language", "en").upper()
            }
    except:
        return None

# ========== SELECTED MOVIE DETAILS ==========
if st.session_state.selected_movie:
    selected_movie = st.session_state.selected_movie
    details = get_movie_details(selected_movie)
    
    if details:
        st.subheader("🎯 Selected Movie")
        col1, col2 = st.columns([1, 2.5])
        with col1:
            if details["poster"]:
                st.image(details["poster"], width=140)
            if st.button("❤️ Add to Favorites", key="fav_main", use_container_width=True):
                if selected_movie not in st.session_state.favorites:
                    st.session_state.favorites.append(selected_movie)
                    st.success("Added to favorites!")
                    st.rerun()
        
        with col2:
            st.markdown(f"### {details['title']}")
            st.markdown(f"📅 {details['release_date']} | ⏱️ {details['runtime']} min | 🌐 {details['language']}")
            st.markdown(f"⭐ Rating: {details['rating']}/10 | 🔥 Popularity: {details['popularity']}")
            st.markdown(f"**Genres:** {', '.join(details['genres'])}")
            
            with st.expander("📖 Story Overview"):
                st.write(details['overview'])
            
            main_trailer = get_trailer_key(selected_movie)
            if main_trailer:
                if st.button("🎬 WATCH TRAILER", key="main_trailer_btn", use_container_width=True):
                    st.session_state.trailer_url = main_trailer
                    st.session_state.trailer_title = details['title']
                    st.rerun()
            else:
                st.info("Trailer not available")
        
        # ========== RECOMMEND BUTTON ==========
        if st.button("🎬 RECOMMEND MOVIES", use_container_width=True):
            with st.spinner("Finding similar movies..."):
                predictor = PredictPipeline()
                st.session_state.recommendations = predictor.recommend(selected_movie)
                st.session_state.show_recommendations = True
                st.session_state.trailer_url = None
                st.session_state.trailer_title = None
                
                if selected_movie not in st.session_state.history:
                    st.session_state.history.append(selected_movie)
                
                st.rerun()

# ========== DISPLAY RECOMMENDATIONS ==========
if st.session_state.show_recommendations and st.session_state.recommendations:
    st.balloons()
    st.success(f"✨ Found {len(st.session_state.recommendations)} recommendations!")
    st.subheader(f"🍿 Movies similar to: **{st.session_state.selected_movie}**")
    st.markdown("---")
    
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🗑️ Clear", key="clear_recs"):
            st.session_state.show_recommendations = False
            st.session_state.recommendations = []
            st.session_state.trailer_url = None
            st.session_state.trailer_title = None
            st.rerun()
    
    rec_data = []
    for idx, movie in enumerate(st.session_state.recommendations[:10]):
        movie_details = get_movie_details(movie)
        if movie_details:
            trailer = get_trailer_key(movie)
            rec_data.append({
                'rank': idx + 1,
                'title': movie,
                'details': movie_details,
                'trailer_key': trailer
            })
    
    for i in range(0, len(rec_data), 5):
        cols = st.columns(5)
        for j in range(5):
            if i + j < len(rec_data):
                data = rec_data[i + j]
                movie_details = data['details']
                movie_title = data['title']
                
                with cols[j]:
                    if movie_details["poster"]:
                        st.image(movie_details["poster"], width=130)
                    
                    st.markdown(f"**{movie_details['title'][:20]}**")
                    st.caption(f"⭐ {movie_details['rating']}/10")
                    
                    if movie_details['genres']:
                        st.caption(f"{', '.join(movie_details['genres'][:2])}")
                    
                    if data['trailer_key']:
                        unique_key = f"rec_trailer_{i}_{j}_{movie_title.replace(' ', '_').replace(':', '')}"
                        if st.button("🎬 Trailer", key=unique_key):
                            st.session_state.trailer_url = data['trailer_key']
                            st.session_state.trailer_title = movie_details['title']
                            st.rerun()
                    else:
                        st.button("🎬 No Trailer", disabled=True, key=f"no_trailer_{i}_{j}")
                    
                    if st.button("❤️", key=f"fav_{i}_{j}_{movie_title}"):
                        if movie_title not in st.session_state.favorites:
                            st.session_state.favorites.append(movie_title)
                            st.success("Added!")
                            st.rerun()
    
    if st.session_state.trailer_url:
        st.markdown("---")
        st.markdown(f"""
        <div class='trailer-container'>
            <h4>🎥 Now Playing: {st.session_state.trailer_title}</h4>
        </div>
        """, unsafe_allow_html=True)
        st.video(f"https://www.youtube.com/watch?v={st.session_state.trailer_url}")
        if st.button("✖️ Close Trailer", key="close_trailer", use_container_width=True):
            st.session_state.trailer_url = None
            st.session_state.trailer_title = None
            st.rerun()
        st.markdown("---")
    
    df = pd.DataFrame([
        {
            'Rank': d['rank'],
            'Movie': d['title'],
            'Rating': d['details']['rating'],
            'Genres': ', '.join(d['details']['genres']),
            'Year': d['details']['release_date'],
            'Popularity': d['details']['popularity']
        }
        for d in rec_data
    ])
    csv = df.to_csv(index=False)
    st.download_button("📥 Download CSV", csv, f"{st.session_state.selected_movie}_recommendations.csv", "text/csv")

# ========== SIDEBAR ==========
with st.sidebar:
    # Favorites Section
    st.markdown("""
    <div class='section-header'>
        <h3>⭐ Favorites</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.favorites:
        st.markdown(f"<span class='favorite-count'>{len(st.session_state.favorites)} movies</span>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        for fav in st.session_state.favorites:
            st.markdown(f"""
            <div class='favorite-card'>
                <div style='display: flex; align-items: center;'>
                    <span class='favorite-emoji'>🎬</span>
                    <span class='favorite-title'>{fav}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button(f"❌ Remove", key=f"remove_{fav}"):
                    st.session_state.favorites.remove(fav)
                    st.rerun()
    else:
        st.info("✨ No favorites yet")
    
    st.markdown("---")
    
    # Recent Searches Section - IMPROVED
    st.markdown("""
    <div class='section-header'>
        <h3>🕐 Recent Searches</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.history:
        # Clear All button with better styling
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"<small style='color: #aaa;'>{len(st.session_state.history)} items</small>", unsafe_allow_html=True)
        with col2:
            if st.button("🗑️ Clear All", key="clear_history", use_container_width=True):
                st.session_state.history = []
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display history items in better format
        for hist in st.session_state.history[-5:][::-1]:  # Reverse to show latest first
            st.markdown(f"""
            <div class='history-card'>
                <div class='history-title'>
                    <span>🎬</span>
                    <span>{hist}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 No recent searches")
    
    st.markdown("---")
    
    # Stats
    st.markdown(f"**📊 Total Movies:** {len(movie_list)}")
    st.markdown(f"**❤️ Favorites:** {len(st.session_state.favorites)}")
    st.markdown(f"**🕐 Recent:** {len(st.session_state.history)}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>🍿 Powered by TMDB | Content-Based Filtering</p>", unsafe_allow_html=True)