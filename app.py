"""
CropGuard Ghana — Crop Disease Detection Chatbot
Helps Ghanaian farmers identify crop diseases and get treatment advice
via a conversational chatbot interface.
"""

from flask import Flask, jsonify, request, render_template
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-prod")


# ---------------------------------------------------------------------------
# Disease Knowledge Base — Ghana's major crops & common diseases
# ---------------------------------------------------------------------------

DISEASE_KB = {
    # ── MAIZE ──────────────────────────────────────────────────────────────
    "maize streak virus": {
        "crop": "maize",
        "aliases": ["streak", "maize streak", "msv", "yellow streaks maize"],
        "symptoms": [
            "Yellow or white streaks running along the leaves",
            "Stunted plant growth",
            "Pale green or chlorotic leaves",
            "Reduced cob size or no cob formation",
        ],
        "cause": "Maize Streak Virus (MSV), transmitted by leafhoppers (Cicadulina spp.)",
        "treatment": [
            "Remove and destroy infected plants immediately",
            "Use MSV-resistant maize varieties (e.g., SEEDCO SC403, Oba Super 9)",
            "Control leafhopper populations with appropriate insecticides",
            "Plant early in the season to avoid peak leafhopper activity",
        ],
        "prevention": [
            "Use certified MSV-resistant seed varieties",
            "Maintain field hygiene — clear crop debris after harvest",
            "Avoid planting near weeds that host leafhoppers",
        ],
        "severity": "High",
        "season": "Year-round; worst during dry season",
    },
    "northern corn leaf blight": {
        "crop": "maize",
        "aliases": ["corn blight", "leaf blight maize", "nclb", "turcicum leaf blight"],
        "symptoms": [
            "Long, cigar-shaped grey-green lesions on leaves",
            "Lesions turn tan/brown as they age",
            "Lesions 2.5–15 cm long with wavy edges",
            "Premature leaf death in severe cases",
        ],
        "cause": "Fungal pathogen Exserohilum turcicum",
        "treatment": [
            "Apply fungicides containing propiconazole or azoxystrobin",
            "Remove heavily infected leaves",
            "Ensure adequate plant spacing for airflow",
        ],
        "prevention": [
            "Plant resistant hybrid varieties",
            "Practice crop rotation (avoid consecutive maize seasons)",
            "Manage crop residue — plough under or burn after harvest",
        ],
        "severity": "Medium–High",
        "season": "Rainy season (May–October)",
    },
    "fall armyworm": {
        "crop": "maize",
        "aliases": ["armyworm", "faw", "caterpillar maize", "worm maize"],
        "symptoms": [
            "Ragged holes in leaves, especially young leaves in the whorl",
            "Frass (sawdust-like droppings) visible in leaf whorl",
            "Caterpillars with an inverted Y on the head",
            "Severe defoliation in heavy infestations",
        ],
        "cause": "Spodoptera frugiperda (invasive moth pest)",
        "treatment": [
            "Apply insecticides: chlorpyrifos, emamectin benzoate, or spinosad",
            "Use biological control: Bacillus thuringiensis (Bt) sprays",
            "Apply sand/soil mixed with ash into the leaf whorl",
            "Spray in the evening when larvae are active",
        ],
        "prevention": [
            "Scout fields regularly (twice a week)",
            "Use pheromone traps to monitor adult moth activity",
            "Intercrop maize with legumes (cowpea, beans)",
            "Encourage natural predators (birds, parasitic wasps)",
        ],
        "severity": "Very High",
        "season": "Year-round; peak in rainy season",
    },

    # ── COCOA ──────────────────────────────────────────────────────────────
    "black pod disease": {
        "crop": "cocoa",
        "aliases": ["black pod", "cocoa black pod", "phytophthora", "pod rot"],
        "symptoms": [
            "Dark brown or black spots on pods that spread rapidly",
            "White fungal growth visible in humid conditions",
            "Infected pods shrivel and harden",
            "Can affect pods at any stage of development",
        ],
        "cause": "Oomycete pathogen Phytophthora palmivora or P. megakarya",
        "treatment": [
            "Apply copper-based fungicides (e.g., copper oxychloride, Ridomil Gold)",
            "Remove and destroy infected pods immediately (do not leave on ground)",
            "Thin canopy to improve airflow and reduce humidity",
        ],
        "prevention": [
            "Regular harvesting — do not leave ripe pods on tree",
            "Prune trees to reduce shade and improve ventilation",
            "Apply fungicide preventively at start of rainy season",
            "Use resistant cocoa varieties from CRIG (Cocoa Research Institute of Ghana)",
        ],
        "severity": "Very High — can destroy 30–90% of crop",
        "season": "Rainy season (peak: September–December)",
    },
    "cocoa swollen shoot virus": {
        "crop": "cocoa",
        "aliases": ["swollen shoot", "cssv", "cocoa virus"],
        "symptoms": [
            "Swelling and distortion of stems and roots",
            "Red vein banding on young leaves",
            "Yellow mosaic patterns on leaves",
            "Severe stunting and eventual tree death",
        ],
        "cause": "Cocoa Swollen Shoot Virus (CSSV), spread by mealybugs",
        "treatment": [
            "No cure — infected trees must be cut out (government compensation available)",
            "Report outbreaks to Ghana Cocoa Board (COCOBOD) immediately",
            "Control mealybug vectors with systemic insecticides",
        ],
        "prevention": [
            "Use CRIG-certified disease-free planting material",
            "Control ant populations (ants protect mealybugs)",
            "Quarantine new planting material before introduction",
        ],
        "severity": "Critical — notifiable disease in Ghana",
        "season": "Year-round",
    },

    # ── CASSAVA ────────────────────────────────────────────────────────────
    "cassava mosaic disease": {
        "crop": "cassava",
        "aliases": ["mosaic", "cassava mosaic", "cmd", "mosaic cassava"],
        "symptoms": [
            "Yellow-green mosaic pattern on leaves",
            "Leaf curling, twisting and distortion",
            "Stunted plant growth",
            "Reduced tuber yield",
        ],
        "cause": "Cassava Mosaic Virus (CMV), spread by whiteflies",
        "treatment": [
            "Remove and destroy severely infected plants",
            "Control whitefly populations with insecticides (imidacloprid)",
            "Replant with clean, certified cuttings",
        ],
        "prevention": [
            "Use CMD-resistant varieties (e.g., Afisiafi, Gblemo Duade)",
            "Source clean planting material from certified nurseries",
            "Control whitefly with yellow sticky traps",
            "Remove volunteer cassava plants from field",
        ],
        "severity": "High",
        "season": "Year-round; spreads rapidly in dry season",
    },
    "cassava bacterial blight": {
        "crop": "cassava",
        "aliases": ["bacterial blight cassava", "cbb", "angular leaf spots cassava"],
        "symptoms": [
            "Angular water-soaked spots on leaves",
            "Leaf blight and wilting",
            "Stem cankers with gummy bacterial ooze",
            "Die-back of shoot tips",
        ],
        "cause": "Bacterium Xanthomonas axonopodis pv. manihotis",
        "treatment": [
            "Remove infected plant material and destroy",
            "Avoid working in fields when plants are wet",
            "Apply copper-based bactericides to stem lesions",
        ],
        "prevention": [
            "Use disease-free planting cuttings",
            "Avoid wounding plants during intercultural operations",
            "Crop rotation with non-host crops",
        ],
        "severity": "Medium–High",
        "season": "Rainy season",
    },

    # ── TOMATO ─────────────────────────────────────────────────────────────
    "tomato late blight": {
        "crop": "tomato",
        "aliases": ["late blight", "tomato blight", "phytophthora tomato"],
        "symptoms": [
            "Water-soaked grey-green spots on leaves that turn brown",
            "White fuzzy mould on underside of leaves in humid weather",
            "Brown firm lesions on fruits",
            "Rapid collapse of entire plant in wet conditions",
        ],
        "cause": "Oomycete Phytophthora infestans",
        "treatment": [
            "Apply fungicides: mancozeb, chlorothalonil, or metalaxyl",
            "Remove and destroy infected plant parts",
            "Avoid overhead irrigation — use drip irrigation",
        ],
        "prevention": [
            "Use resistant varieties (e.g., Pectomech, Petomech F1)",
            "Stake plants to improve air circulation",
            "Spray preventive fungicides at start of season",
            "Avoid planting in low-lying areas with poor drainage",
        ],
        "severity": "Very High",
        "season": "Rainy season / cool humid conditions",
    },
    "tomato leaf curl": {
        "crop": "tomato",
        "aliases": ["leaf curl tomato", "tomato curl", "tylcv"],
        "symptoms": [
            "Upward curling and yellowing of leaves",
            "Stunted and bushy plant growth",
            "Small, poorly set fruits",
            "Leaf edges turn purple in some varieties",
        ],
        "cause": "Tomato Yellow Leaf Curl Virus (TYLCV), spread by whiteflies",
        "treatment": [
            "Remove and destroy infected plants",
            "Apply systemic insecticides to control whiteflies",
            "Use reflective mulches to repel whiteflies",
        ],
        "prevention": [
            "Plant resistant varieties",
            "Use insect-proof nets in nurseries",
            "Avoid transplanting seedlings from infected nurseries",
        ],
        "severity": "High",
        "season": "Dry season (whitefly population peaks)",
    },

    # ── YAM ────────────────────────────────────────────────────────────────
    "yam anthracnose": {
        "crop": "yam",
        "aliases": ["anthracnose yam", "yam blight", "yam leaf spot"],
        "symptoms": [
            "Dark brown irregular lesions on leaves",
            "Lesions with yellow halos",
            "Dieback of vines from leaf tips",
            "Defoliation in severe cases",
        ],
        "cause": "Fungal pathogen Colletotrichum gloeosporioides",
        "treatment": [
            "Apply fungicides: mancozeb or carbendazim",
            "Remove and destroy infected vines",
            "Improve staking to reduce vine contact with soil",
        ],
        "prevention": [
            "Use disease-free seed yam",
            "Practice crop rotation",
            "Avoid high humidity by proper spacing",
        ],
        "severity": "Medium",
        "season": "Rainy season",
    },
}

# ---------------------------------------------------------------------------
# Chatbot engine
# ---------------------------------------------------------------------------

GREETINGS = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening",
             "akwaaba", "ete sen", "me ho ye", "salama"]

FAREWELLS = ["bye", "goodbye", "thank you", "thanks", "daabi", "medaase", "exit", "quit"]

HELP_TRIGGERS = ["help", "what can you do", "how do you work", "commands", "menu"]

CROP_LIST_TRIGGERS = ["crops", "which crops", "what crops", "supported crops", "list crops"]

SEVERITY_INFO = {
    "Very High": "🔴",
    "Critical — notifiable disease in Ghana": "🚨",
    "High": "🟠",
    "Medium–High": "🟡",
    "Medium": "🟢",
}


def build_greeting_response() -> dict:
    return {
        "type": "greeting",
        "message": (
            "Akwaaba! 👋 I'm **CropGuard**, your AI farming assistant for Ghana.\n\n"
            "I can help you **identify crop diseases**, understand their **symptoms**, "
            "and get **treatment advice** — all tailored for Ghanaian crops.\n\n"
            "**Try asking me:**\n"
            "• *My maize leaves have yellow streaks — what's wrong?*\n"
            "• *How do I treat black pod disease in cocoa?*\n"
            "• *What pests affect cassava?*\n"
            "• *List all crops you support*"
        ),
    }


def build_help_response() -> dict:
    return {
        "type": "help",
        "message": (
            "**Here's what I can help you with:**\n\n"
            "🌿 **Describe symptoms** — tell me what you see on your crop (colour, shape, location of damage)\n"
            "🔍 **Ask by disease name** — e.g. *'Tell me about fall armyworm'*\n"
            "🌾 **Ask by crop** — e.g. *'What diseases affect cocoa?'*\n"
            "💊 **Ask for treatment** — e.g. *'How do I treat maize streak?'*\n\n"
            "**Supported crops:** Maize, Cocoa, Cassava, Tomato, Yam\n\n"
            "Type **'list crops'** to see all supported diseases by crop."
        ),
    }


def build_crop_list_response() -> dict:
    by_crop: dict[str, list[str]] = {}
    for disease, data in DISEASE_KB.items():
        crop = data["crop"].capitalize()
        by_crop.setdefault(crop, []).append(disease.title())

    lines = ["**Crops and diseases I know about:**\n"]
    crop_icons = {"Maize": "🌽", "Cocoa": "🍫", "Cassava": "🥔", "Tomato": "🍅", "Yam": "🍠"}
    for crop, diseases in sorted(by_crop.items()):
        icon = crop_icons.get(crop, "🌿")
        lines.append(f"{icon} **{crop}**")
        for d in diseases:
            lines.append(f"   • {d}")
    return {"type": "crop_list", "message": "\n".join(lines)}


def match_disease(user_input: str) -> list[str]:
    """Find matching diseases from user input using keyword matching."""
    text = user_input.lower()
    matches = []

    for disease_key, data in DISEASE_KB.items():
        # Check disease name
        if disease_key in text:
            matches.append(disease_key)
            continue
        # Check aliases
        if any(alias in text for alias in data.get("aliases", [])):
            matches.append(disease_key)
            continue
        # Check crop name + symptom keywords
        symptom_words = " ".join(data["symptoms"]).lower()
        crop = data["crop"]
        if crop in text:
            # Check for symptom keywords
            symptom_keywords = [
                w for w in text.split()
                if len(w) > 4 and w in symptom_words
            ]
            if symptom_keywords:
                matches.append(disease_key)

    return list(dict.fromkeys(matches))  # deduplicate preserving order


def match_crop(user_input: str) -> str | None:
    crops = ["maize", "cocoa", "cassava", "tomato", "yam", "corn"]
    text = user_input.lower()
    for crop in crops:
        if crop in text:
            return "maize" if crop == "corn" else crop
    return None


def build_disease_response(disease_key: str) -> dict:
    d = DISEASE_KB[disease_key]
    severity_icon = SEVERITY_INFO.get(d["severity"], "⚪")

    symptoms_str = "\n".join(f"  • {s}" for s in d["symptoms"])
    treatment_str = "\n".join(f"  {i+1}. {t}" for i, t in enumerate(d["treatment"]))
    prevention_str = "\n".join(f"  • {p}" for p in d["prevention"])

    message = (
        f"## {disease_key.title()}\n"
        f"**Crop:** {d['crop'].capitalize()} &nbsp; | &nbsp; "
        f"**Severity:** {severity_icon} {d['severity']} &nbsp; | &nbsp; "
        f"**Peak Season:** {d['season']}\n\n"
        f"**🦠 Cause:**\n  {d['cause']}\n\n"
        f"**🔍 Symptoms:**\n{symptoms_str}\n\n"
        f"**💊 Treatment:**\n{treatment_str}\n\n"
        f"**🛡️ Prevention:**\n{prevention_str}"
    )
    return {"type": "disease_info", "disease": disease_key, "message": message}


def build_crop_diseases_response(crop: str) -> dict:
    diseases = {k: v for k, v in DISEASE_KB.items() if v["crop"] == crop}
    crop_icons = {"maize": "🌽", "cocoa": "🍫", "cassava": "🥔", "tomato": "🍅", "yam": "🍠"}

    if not diseases:
        return {"type": "not_found", "message": f"I don't have disease data for {crop} yet."}

    icon = crop_icons.get(crop, "🌿")
    lines = [f"{icon} **Diseases affecting {crop.capitalize()} in Ghana:**\n"]
    for name, data in diseases.items():
        sev_icon = SEVERITY_INFO.get(data["severity"], "⚪")
        lines.append(f"**{name.title()}** {sev_icon}")
        lines.append(f"  _{data['symptoms'][0]}_")
        lines.append(f"  Ask me: *'Tell me about {name}'* for full details\n")

    return {"type": "crop_diseases", "crop": crop, "message": "\n".join(lines)}


def build_not_found_response(user_input: str) -> dict:
    # Suggest possible crops
    crop = match_crop(user_input)
    hint = (
        f"\n\nYou mentioned **{crop}** — try asking: *'What diseases affect {crop}?'*"
        if crop else
        "\n\nTry describing **symptoms** (e.g. *yellow leaves, spots, wilting*) "
        "or ask about a **specific crop** (maize, cocoa, cassava, tomato, yam)."
    )
    return {
        "type": "not_found",
        "message": (
            "I'm not sure which disease you're describing. "
            "Could you give me more detail?" + hint
        ),
    }


def process_message(user_input: str) -> dict:
    """Main chatbot logic — classify input and return structured response."""
    if not user_input or not user_input.strip():
        return {"type": "error", "message": "Please type a message!"}

    text = user_input.lower().strip()

    # Greetings
    if any(g in text for g in GREETINGS):
        return build_greeting_response()

    # Farewells
    if any(f in text for f in FAREWELLS):
        return {
            "type": "farewell",
            "message": "Medaase! 🙏 Take good care of your crops. Come back anytime — CropGuard is here to help!",
        }

    # Help
    if any(h in text for h in HELP_TRIGGERS):
        return build_help_response()

    # Crop list
    if any(t in text for t in CROP_LIST_TRIGGERS):
        return build_crop_list_response()

    # Explicit crop-level query takes priority (e.g. "what diseases affect cocoa")
    CROP_QUERY_PATTERNS = ["diseases affect", "diseases in", "diseases on", "affect", "pests affect"]
    crop = match_crop(text)
    if crop and any(p in text for p in CROP_QUERY_PATTERNS):
        return build_crop_diseases_response(crop)

    # Disease match
    matched = match_disease(text)
    if len(matched) == 1:
        return build_disease_response(matched[0])
    if len(matched) > 1:
        # Multiple matches — ask to clarify
        options = "\n".join(f"• *{d.title()}*" for d in matched[:4])
        return {
            "type": "clarify",
            "message": (
                f"I found **{len(matched)} possible diseases** matching your description:\n\n"
                + options
                + "\n\nCould you tell me more? Or click one above to learn more."
            ),
            "matches": matched,
        }

    # Crop-level query (no disease keywords)
    if crop:
        return build_crop_diseases_response(crop)

    return build_not_found_response(user_input)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    body = request.get_json(silent=True) or {}
    user_message = body.get("message", "").strip()

    if not user_message:
        return jsonify({"status": "error", "message": "No message provided"}), 400

    response = process_message(user_message)
    return jsonify({
        "status": "success",
        "response": response,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    })


@app.route("/api/diseases", methods=["GET"])
def list_diseases():
    """Return all diseases in the knowledge base."""
    crop_filter = request.args.get("crop", "").lower()
    data = {
        k: {
            "crop": v["crop"],
            "severity": v["severity"],
            "season": v["season"],
            "symptom_count": len(v["symptoms"]),
        }
        for k, v in DISEASE_KB.items()
        if not crop_filter or v["crop"] == crop_filter
    }
    return jsonify({"status": "success", "count": len(data), "diseases": data})


@app.route("/api/diseases/<disease_name>", methods=["GET"])
def get_disease(disease_name: str):
    key = disease_name.lower().replace("-", " ")
    if key not in DISEASE_KB:
        return jsonify({"status": "error", "message": f"Disease '{disease_name}' not found"}), 404
    return jsonify({"status": "success", "disease": key, "data": DISEASE_KB[key]})


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "CropGuard Ghana Chatbot API",
        "version": "1.0.0",
        "diseases_in_kb": len(DISEASE_KB),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV", "development") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)

