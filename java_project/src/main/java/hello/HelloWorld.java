package hello;

/**
 * Класс HelloWorld содержит основной метод, который запускает приложение.
 */
public class HelloWorld {
  
    /**
     * Основной метод, который служит точкой входа в приложение.
     *
     * @param args Аргументы командной строки (не используются).
     */
    public static void main(String[] args) {
        Greeter greeter = new Greeter();
        System.out.println(greeter.sayHello());

        MultilingualGreeter multilingualGreeter = new MultilingualGreeter();
        System.out.println(multilingualGreeter.sayHello("es")); // Приветствие на испанском
        System.out.println(multilingualGreeter.sayHello("fr")); // Приветствие на французском
        System.out.println(multilingualGreeter.sayHello("de")); // Приветствие на немецком
        System.out.println(multilingualGreeter.sayHello("it")); // Приветствие на итальянском (по умолчанию на английском)
    }
}
