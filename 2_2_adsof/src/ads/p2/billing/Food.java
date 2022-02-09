package ads.p2.billing;

/**
 * 
 * @author ADSOF teachers
 *
 */
public class Food extends Article {
	private boolean promo3x2;
	
	public Food(long id, String desc, double price, boolean promo) {
		super(id, desc, price);
		promo3x2 = promo;
	}
	
	/**
	 * Getter for the promo
	 * @return true if it has the promotion
	 */
	public boolean getPromo3x2() { return promo3x2; }
	
	/**
	 * Setter for the promo
	 * @param promo
	 */
	public void setPromo3x2(boolean promo) { promo3x2 = promo; }
	
	/**
	 * Getter of the typeVAT
	 * @return 0.10
	 */
	public double typeVAT() { return 0.10; }
	
	/**
	 * Calculator of the discount
	 * @param units Number of products
	 * @return discount
	 */
	public double discount(double units) {
		if (promo3x2) return getUnitPrice() * (int) (units / 3);
		else return 0.0;		
	}
}

