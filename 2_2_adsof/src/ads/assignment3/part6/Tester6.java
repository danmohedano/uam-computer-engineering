/**
 * 
 */
package ads.assignment3.part6;

import java.util.*;

/**
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
public class Tester6 {
	public static void main(String[] args) {
		List<Appliance> created = new ArrayList<>();
		List<Sale> salesCreated = new ArrayList<>();
		
		System.out.println("Creating 5 new TV................");
		for (int i = 1; i <= 5; ++i)
		{
			created.add(new Television("TV", String.valueOf(i), i*1000, EnergyEfficiency.A, 40));
		}
		
		System.out.println("Creating 5 identical washers.............");
		for (int i = 1; i <= 5; ++i)
		{
			created.add(new Washer("Washer", "X", 400.0, EnergyEfficiency.B, new Dimension(10, 10, 10), 50));
		}
		
		System.out.println(StockItem.getStock());
		
		System.out.println("Creating sale for 1st TV................");
		try {
			salesCreated.add(new Sale(created.get(0)));
		}catch(Exception e) {
			System.out.println("Unable to create sale.\n");
		}
		
		System.out.println(Sale.salesSummary());
		
		System.out.println("Creating sale for 1st TV again...................");
		try {
			salesCreated.add(new Sale(created.get(0)));
		}catch(Exception e) {
			System.out.println("Unable to create sale.\n");
		}
		
		System.out.println(Sale.salesSummary());
		
		System.out.println("Creating sale for 2 washers....................");
		for(int i = 0; i < 2; ++i)
		{
			try {
				salesCreated.add(new Sale(created.get(5 + i)));
			}catch (Exception e) {
				System.out.println("Unable to create sale.\n");
			}
		}
		
		System.out.println(Sale.salesSummary());
		System.out.println(StockItem.getStock());
		
		Sale.cancel();
		System.out.println("State after cancelling sale:\n");
		System.out.println(Sale.salesSummary());
		System.out.println(StockItem.getStock());
	}

}
