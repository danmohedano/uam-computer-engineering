package ads.p2.billing;

/**
 * 
 * @author ADSOF teachers
 *
 */
public abstract class Article {
	private long identifier;
	private String description;
	private double unitPrice;
	
	public Article(long id, String desc, double price) {
		identifier = id; 
		description = desc; 
		unitPrice = price;
	}
	
	/**
	 * Getter for the identifier
	 * @return identifier
	 */
	public long getIdentifier() { return identifier; }
	
	/**
	 * Getter for the description
	 * @return description
	 */
	public String getDescription() { return description; }
	
	/**
	 * Getter for the unit price
	 * @return unit price
	 */
	public double getUnitPrice() { return unitPrice; }
	
	/**
	 * Setter for the description
	 * @param desc Description to save
	 */
	public void setDescription(String desc) { description = desc; }
	
	/**
	 * Setter for the unit price
	 * @param price Unit price
	 */
	public void setUnitPrice(double price) { unitPrice = price; }
		
	// The general VAT 21%, unless it is redefined in subclasses
	/**
	 * Getter for the typeVAT
	 * @return 0.21
	 */
	public double typeVAT() { return 0.21; }
	
	// Every subclass of Article will calculate the corresponding discount
	public abstract double discount(double units);
	
	// Total price is always calculated in the same way
	/**
	 * Calculator for the total price of the product
	 * @param units Amount of articles
	 * @return total price
	 */
	public double totalPrice(double units) {
		return ((unitPrice * units) - discount(units)) 
                     * (1.0 + typeVAT());
	}

	public String toString(){
		return "Id:" + identifier + " " + description +  " Price: " + unitPrice;
	}
}

 