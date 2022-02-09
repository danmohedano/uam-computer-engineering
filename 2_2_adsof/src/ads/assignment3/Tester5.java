package ads.assignment3;

/**
 * Tester for Part 5 of lab assignment 3
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
public class Tester5 {

	public static void main(String[] args) {
		Appliance tv1 = new CurvedTelevision("Television", "Curved Model", 1699.00, EnergyEfficiency.A, 40, new Dimension(100, 100, 100), 50);

		Sale s1 = new Sale(tv1);							//Regular sale of the TV (no shipping cost)
		Sale s2 = new HomeDeliverySale(tv1);				//Regular home delivered sale of the tv (shipping cost equal to 25 per cubic meter)
		Sale s3 = new HomeDeliveredCanaryIslandSale(tv1);	//Canary island home delivered sale of the tv (shipping cost equal to 7% of the base price)
		
		System.out.println(s1.getTicket());
		System.out.println(s2.getTicket());
		System.out.println(s3.getTicket());
	}

}
