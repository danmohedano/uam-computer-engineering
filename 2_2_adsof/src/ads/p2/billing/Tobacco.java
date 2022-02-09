package ads.p2.billing;

/**
 * 
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 * 
 */
public class Tobacco extends Article {

    public Tobacco(long id, String desc, double price) {
        super(id, desc, price);
    }
         
    /**
     * Calculator for the total price of the tobacco
     * 
     * @param units Amount of tobacco
     * @return total price
     */
    public double totalPrice(double units) {
        return (getUnitPrice() * units) * (1.0 + typeVAT());
    }

    /**
     * Discount for the tobacco (always 0)
     * 
     * @return 0
     */
    public double discount(double units){ return 0; }
    
}
