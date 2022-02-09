package ads.p2;

import ads.p2.billing.*;

/**
 * 
 * @author ADSOF teachers
 * 
 * Application entry point to test original classes
 */
public class Example1 {
	public static void main(String args[]) {
		Article a1 = new Food(990034, "Chocolate", 2.5, true);
		System.out.println("Total price: "+ a1.totalPrice(7)); // 13.75 = (7 * 2.5 - 2 * 2.5) * 1.10
		Food a2 = new Food(990268, "Yoghourt", 1.25, false);
		System.out.println("Total price: "	+ a2.totalPrice(4)); // 5.5 = (4 * 1.25 - 0.0) * 1.10

	}
}