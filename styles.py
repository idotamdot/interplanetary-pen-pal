# ======================================
# 🌌 COSMIC STYLES & ANIMATIONS
# ======================================

def get_cosmic_css():
    """Returns custom CSS for cosmic aesthetics and animations"""
    return """
    <style>
    /* Animated Starfield Background */
    @keyframes twinkle {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    @keyframes glow {
        0%, 100% { text-shadow: 0 0 10px rgba(108, 99, 255, 0.5); }
        50% { text-shadow: 0 0 20px rgba(108, 99, 255, 0.8), 0 0 30px rgba(108, 99, 255, 0.6); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Main Content Animation */
    .main .block-container {
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Glowing Headers */
    h1, h2, h3 {
        animation: glow 3s ease-in-out infinite;
        background: linear-gradient(90deg, #6C63FF, #9D8FFF, #6C63FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 200% auto;
        animation: shimmer 3s linear infinite, glow 3s ease-in-out infinite;
    }
    
    /* Cosmic Dividers */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #6C63FF, transparent);
        margin: 2rem 0;
        animation: shimmer 3s linear infinite;
        background-size: 200% auto;
    }
    
    /* Button Enhancements */
    .stButton > button {
        background: linear-gradient(135deg, #6C63FF, #9D8FFF);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(108, 99, 255, 0.6);
    }
    
    /* Text Input Enhancements */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 1px solid rgba(108, 99, 255, 0.3);
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6C63FF;
        box-shadow: 0 0 15px rgba(108, 99, 255, 0.3);
    }
    
    /* Selectbox Enhancement */
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    /* Cosmic Cards */
    .cosmic-card {
        background: linear-gradient(135deg, rgba(108, 99, 255, 0.1), rgba(157, 143, 255, 0.05));
        border: 1px solid rgba(108, 99, 255, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .cosmic-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(108, 99, 255, 0.3);
        border-color: rgba(108, 99, 255, 0.6);
    }
    
    /* Expander Enhancement */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(108, 99, 255, 0.1), rgba(157, 143, 255, 0.05));
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(108, 99, 255, 0.2), rgba(157, 143, 255, 0.1));
    }
    
    /* Sidebar Enhancement */
    .css-1d391kg {
        background: linear-gradient(180deg, #0E0E2C, #1C1C3C);
    }
    
    /* Success/Info/Warning Messages */
    .stSuccess, .stInfo, .stWarning {
        border-radius: 10px;
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Floating Stars Decoration */
    .star-decoration {
        position: fixed;
        pointer-events: none;
        font-size: 20px;
        animation: float 3s ease-in-out infinite, twinkle 2s ease-in-out infinite;
        z-index: -1;
    }
    
    /* Cosmic Quote Box */
    .cosmic-quote {
        background: linear-gradient(135deg, rgba(108, 99, 255, 0.15), rgba(157, 143, 255, 0.08));
        border-left: 4px solid #6C63FF;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 0 15px 15px 0;
        font-style: italic;
        animation: fadeIn 1s ease-out;
    }
    
    /* Metric Enhancement */
    [data-testid="stMetricValue"] {
        background: linear-gradient(90deg, #6C63FF, #9D8FFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 3s ease-in-out infinite;
    }
    
    /* Tab Enhancement */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
    }
    
    /* Link Enhancement */
    a {
        color: #9D8FFF;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    
    a:hover {
        color: #6C63FF;
        text-shadow: 0 0 10px rgba(108, 99, 255, 0.5);
    }
    
    /* Smooth Scrolling */
    html {
        scroll-behavior: smooth;
    }
    </style>
    """

def get_starfield_html():
    """Returns HTML/JS for animated starfield background"""
    return """
    <div id="starfield"></div>
    <script>
    function createStarfield() {
        const starfield = document.getElementById('starfield');
        if (!starfield || starfield.children.length > 0) return;
        
        starfield.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            overflow: hidden;
        `;
        
        for (let i = 0; i < 50; i++) {
            const star = document.createElement('div');
            star.style.cssText = `
                position: absolute;
                width: 2px;
                height: 2px;
                background: white;
                border-radius: 50%;
                top: ${Math.random() * 100}%;
                left: ${Math.random() * 100}%;
                opacity: ${Math.random() * 0.5 + 0.2};
                animation: twinkle ${Math.random() * 3 + 2}s ease-in-out infinite;
                animation-delay: ${Math.random() * 2}s;
            `;
            starfield.appendChild(star);
        }
    }
    
    createStarfield();
    </script>
    """
