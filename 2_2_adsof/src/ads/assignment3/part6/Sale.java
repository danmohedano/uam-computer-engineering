package ads.assignment3.part6;

import java.util.*;

/**
 * Sale class
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 */
public class Sale {
    private Appliance purchasedAppliance;
	private Appliance deliveredAppliance;
	private static List <Sale> sales = new ArrayList<Sale>();
    
    public Sale(Appliance purchased) throws Exception
    {
		purchasedAppliance = purchased;
		if (StockItem.removeFromStock(purchased) == -1) throw new Exception("Appliance not in stock");
		Sale.sales.add(this);
    }

    public Sale(Appliance purchased, Appliance delivered) throws Exception
    {
        this(purchased);
		deliveredAppliance = delivered;
    }

    /**
     * Method to calculate the final cost of the sale
     * @return the final cost
     */
    public double finalCost()
    {
    	return purchasedAppliance.getBasePrice() - this.discount();
    }
	
	/**
	 * Discount of the sale
	 * @return the discount
	 */
    public double discount()
    {
    	if (deliveredAppliance == null) return 0.0;
    	else if (deliveredAppliance.getEfficiency().compareTo(EnergyEfficiency.UNKNOWN) == 0) return 10.0;
    	else if (purchasedAppliance.getEfficiency().compareTo(EnergyEfficiency.UNKNOWN) != 0)
    	{
    		if (purchasedAppliance.getEfficiency().compareTo(deliveredAppliance.getEfficiency()) == 0) return 25.0;
    		else if (purchasedAppliance.getEfficiency().compareTo(deliveredAppliance.getEfficiency()) < 0) return 25.0 + (deliveredAppliance.getEfficiency().compareTo(purchasedAppliance.getEfficiency()))*15.0;
    		else return 25.0 + (deliveredAppliance.getEfficiency().compareTo(purchasedAppliance.getEfficiency()))*5.0;
    	}
    	return 0.0;
	}
	
	/**
	 * Purchased Appliance as string for the ticket
	 * @return purchased appliance as string
	 */
	public String getPurchasedApplianceAsString()
	{
		return 	"--------------------------------------------\n" + 
				"Sold product: " + purchasedAppliance + "\n" +
				"--------------------------------------------\n";
	}
	
	/**
	 * Base Price of the appliance as a string
	 * @return base price as string
	 */
	public String getBasePriceAsString()
	{
		return "Product price:\t\t" + String.format("%10.2f", purchasedAppliance.getBasePrice()) + "\n";
	}
	
	/**
	 * Discount of the sale as a string
	 * @return discount as string
	 */
	public String discountAsString()
	{
		return "Shipping discount:\t" + String.format("%10.2f", discount()) + "\n";
	}

	/**
	 * Final Cost of the sale as a string
	 * @return final cost as string
	 */
	public String finalCostAsString()
	{
		return "TOTAL:\t\t\t" + String.format("%10.2f", finalCost()) + "\n";
	}
	

	/**
	 * Ticket of a sale
	 * @return the ticket
	 */
    public String getTicket()
    {
    	return 	this.getPurchasedApplianceAsString() +
    			this.getBasePriceAsString() +
    			this.discountAsString() +
    			this.finalCostAsString();
    }

	/**
	 * @return the purchasedAppliance
	 */
	public Appliance getPurchasedAppliance() {
		return purchasedAppliance;
	}

	/**
	 * @param purchasedAppliance the purchasedAppliance to set
	 */
	public void setPurchasedAppliance(Appliance purchasedAppliance) {
		this.purchasedAppliance = purchasedAppliance;
	}

	/**
	 * @return the deliveredAppliance
	 */
	public Appliance getDeliveredAppliance() {
		return deliveredAppliance;
	}

	/**
	 * @param deliveredAppliance the deliveredAppliance to set
	 */
	public void setDeliveredAppliance(Appliance deliveredAppliance) {
		this.deliveredAppliance = deliveredAppliance;
	}
	
	/**
	 * Summary of all sales done
	 * @return  the summary
	 */
	public static String salesSummary()
	{
		String summary = "SALES SUMMARY\n";
		for(Sale s: Sale.sales){
			summary += s.finalCostAsString();
		}
		return summary;
	}
	
	/**
	 * Summary of all sales with cost bigger than the limit
	 * @param limit
	 * @return the summary
	 */
	public static String salesSummary(double limit)
	{
		String summary = "SALES SUMMARY\n";
		for(Sale s: Sale.sales){
			if (s.finalCost() >= limit)
			{
				summary += s.finalCostAsString();
			}
		}
		return summary;
	}
	
	/**
	 * Summary of all sales of products whose brand contains the text
	 * @param text
	 * @return the summary
	 */
	public static String salesSummary(String text)
	{
		String summary = "SALES SUMMARY\n";
		for(Sale s: Sale.sales){
			if (s.getPurchasedAppliance().getBrand().contains(text))
			{
				summary += s.finalCostAsString();
			}
		}
		return summary;
	}

	/**
	 * Cancels the last sale added to the collection
	 * @return the cancelled sale
	 */
	public static Sale cancel(){
		if(Sale.sales.isEmpty() == true) return null;
		Sale cancelled = Sale.sales.remove(Sale.sales.size() - 1);
		StockItem.addToStock(cancelled.purchasedAppliance);
		return cancelled;
	}
	/**
	 * Last sale added to the collection
	 * @return the last added sale
	 */
	public static Sale last(){
		return Sale.sales.get(Sale.sales.size() - 1);
	}
}
