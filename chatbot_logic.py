# chatbot_logic.py
import json
from difflib import SequenceMatcher
from typing import List, Tuple, Dict, Optional

class ChatbotLogic:
    def __init__(self, chat_window):
        self.chat_window = chat_window
        self.faq_data = self.load_faq()
        self.similarity_threshold = 0.6
        # Düz soru-cevap listesi oluştur
        self.flat_qa_dict = self._flatten_faq()

    def load_faq(self) -> dict:
        try:
            with open("faq.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            self.chat_window.append("Sık sorulan sorular dosyası bulunamadı.")
            return {"categories": {}}

    def _flatten_faq(self) -> Dict[str, str]:
        """FAQ yapısını düz bir soru-cevap sözlüğüne çevirir."""
        flat_dict = {}
        for category in self.faq_data["categories"].values():
            flat_dict.update(category["questions"])
        return flat_dict

    def get_categories(self) -> List[Dict[str, str]]:
        """Tüm kategorileri başlıklarıyla birlikte döndürür."""
        return [
            {"id": cat_id, "title": data["title"]}
            for cat_id, data in self.faq_data["categories"].items()
        ]

    def get_questions_by_category(self, category_id: str) -> Dict[str, str]:
        """Belirli bir kategorideki tüm soru ve cevapları döndürür."""
        try:
            return self.faq_data["categories"][category_id]["questions"]
        except KeyError:
            return {}

    def calculate_similarity(self, text1: str, text2: str) -> float:
        text1 = ' '.join(text1.lower().split())
        text2 = ' '.join(text2.lower().split())
        return SequenceMatcher(None, text1, text2).ratio()

    def preprocess_message(self, message: str) -> str:
        message = message.lower()
        message = ' '.join(message.split())
        return message

    def find_best_matches(self, message: str, top_n: int = 3) -> List[Tuple[str, float]]:
        message = self.preprocess_message(message)
        matches = []

        for question in self.flat_qa_dict.keys():
            similarity = self.calculate_similarity(message, question)
            if similarity >= self.similarity_threshold:
                matches.append((question, similarity))

        return sorted(matches, key=lambda x: x[1], reverse=True)[:top_n]

    def find_category_for_question(self, question: str) -> Optional[str]:
        """Bir sorunun hangi kategoride olduğunu bulur."""
        for cat_id, category in self.faq_data["categories"].items():
            if question in category["questions"]:
                return category["title"]
        return None

    def process_message(self, message: str) -> str:
        # Direkt eşleşme kontrolü
        if message in self.flat_qa_dict:
            response = self.flat_qa_dict[message]
            category = self.find_category_for_question(message)
            if category:
                return f"[{category}]\n\n{response}"
            return response

        best_matches = self.find_best_matches(message)

        if best_matches:
            if best_matches[0][1] > 0.8:
                response = self.flat_qa_dict[best_matches[0][0]]
                category = self.find_category_for_question(best_matches[0][0])
                if category:
                    return f"[{category}]\n\n{response}"
                return response

            suggestions = []
            for match, _ in best_matches:
                category = self.find_category_for_question(match)
                if category:
                    suggestions.append(f"[{category}] {match}")
                else:
                    suggestions.append(match)

            return (
                "Tam olarak ne demek istediğinizi anlayamadım. "
                "Belki şunlardan birini sormak istemiş olabilirsiniz:\n\n" +
                "\n".join(f"- {s}" for s in suggestions)
            )

        return (
            "Üzgünüm, sorunuza uygun bir yanıt bulamadım. "
            "Lütfen sorunuzu farklı bir şekilde sormayı deneyin veya "
            "kategorilerden birini seçerek ilgili soruları görüntüleyin."
        )