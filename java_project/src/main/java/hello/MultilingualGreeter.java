package hello;

import java.util.HashMap;
import java.util.Map;

/**
 * Класс MultilingualGreeter предоставляет приветствия на нескольких языках.
 */
public class MultilingualGreeter {
    private Map<String, String> greetings;

    /**
     * Конструктор MultilingualGreeter инициализирует карту приветствий.
     */
    public MultilingualGreeter() {
        greetings = new HashMap<>();
        greetings.put("en", "Hello world!");
        greetings.put("es", "¡Hola mundo!");
        greetings.put("fr", "Bonjour le monde!");
        greetings.put("de", "Hallo Welt!");
    }

    /**
     * Возвращает приветственное сообщение на указанном языке.
     *
     * @param language Код языка (например, "en", "es", "fr", "de").
     * @return Приветственное сообщение на указанном языке, или на английском, если язык не поддерживается.
     */
    public String sayHello(String language) {
        return greetings.getOrDefault(language, greetings.get("en"));
    }
}
