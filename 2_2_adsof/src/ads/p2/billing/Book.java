package ads.p2.billing;

/**
 * 
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 * 
 */
public class Book extends Article {
    private String category;

    public Book(long id, String desc, double price, String cat){
        super(id, desc, price);
        category = cat;
    }

    /**
     * Getter of the category of the book
     * 
     * @return category of the book
     */
    public String getCategory(){ return category; }
    
    /**
     * Setter of the category of the book
     * 
     * @param cat category of the book
     */
    public void setCategory(String cat){ category = cat; }
    
    public double typeVAT(){ return 0.04; }
    
    /**
     * Calculates the discount of the book.
     * 
     * @param units Number of books
     * @return discount
     */
    public double discount(double units){
        if (category == "Textbook") { return getUnitPrice() * units * 0.15; }
        if (category == "Collection") {
            if (units > 2) {
                return getUnitPrice() * (units - 2) * 0.5;
            }
            else { return 0; }
        }
        else { return 0; } 
    }

}