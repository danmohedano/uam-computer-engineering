/**
 * 
 */
package ads.assignment3.part6;

import java.util.*;

/**
 * @author Daniel Mohedano & Silvia Sopeña
 *
 */
public class StockItem {

	private static List<StockItem> stock = new ArrayList<>();
	private Appliance 	item;
	private int 		quantity;
	
	private StockItem(Appliance item)
	{
		this.item = item;
		quantity = 1;
	}
	
	/**
	 * Adds an appliance to the stock
	 * @param app - Appliance to add to stock
	 * @return quantity of the appliance available in stock
	 */
	public static int addToStock(Appliance app)
	{
		StockItem s = new StockItem(app);
		if (!StockItem.stock.contains(s)) 
		{
			StockItem.stock.add(s);
			return 1;
		}
		else
		{
			StockItem.stock.get(StockItem.stock.indexOf(s)).quantity += 1;
			return StockItem.stock.get(StockItem.stock.indexOf(s)).quantity;
		}
	}
	
	/**
	 * Removes an appliance from the stock
	 * @param app - Appliance to remove
	 * @return quantity of the appliance in stock, -1 if error
	 */
	public static int removeFromStock(Appliance app)
	{
		StockItem s = new StockItem(app);
		if (!StockItem.stock.contains(s)) return -1;
		else
		{
			if (StockItem.stock.get(StockItem.stock.indexOf(s)).quantity == 1)
			{
				StockItem.stock.remove(s);
				return 0;
			}
			else 
			{
					StockItem.stock.get(StockItem.stock.indexOf(s)).quantity -= 1;
					return StockItem.stock.get(StockItem.stock.indexOf(s)).quantity;
			}
		}
	}
	
	/**
	 * Returns the full stock
	 * @return stock as string
	 */
	public static String getStock()
	{
		String s = "CURRENT STOCK\n";
		for (StockItem si : StockItem.stock)
		{
			s += si.item + " [" + si.quantity + "]" + "\n";
		}
		return s;
	}
	
	public boolean equals(Object obj)
	{
		if (obj == null || obj.getClass() != this.getClass()) return false;

		if (this.item.equals(((StockItem)obj).item)) return true;
		return false;
	}
	
}
