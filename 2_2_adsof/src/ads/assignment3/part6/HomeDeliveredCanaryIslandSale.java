/**
 * 
 */
package ads.assignment3.part6;

/**
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 *
 */
public class HomeDeliveredCanaryIslandSale extends CanaryIslandSale {

	public HomeDeliveredCanaryIslandSale(Appliance purchased) throws Exception
	{
		super(purchased);
	}
	
	public double finalCost()
	{
		return super.finalCost() + (this.getPurchasedAppliance().getBasePrice() * 0.07);
	}
	
	/**
     * Transport Cost of the appliance as a string
     * @return transport cost as string
     */
    public String getTransportCostAsString()
    {
        return "Shippin cost:\t\t" + String.format("%10.2f", getPurchasedAppliance().getBasePrice() * 0.07) + "\n";
    }
	
	/**
     * Ticket of the home delivered canary island sale
     * @return the ticket
     */
    @Override
    public String getTicket()
    {
    	return 	this.getPurchasedApplianceAsString() +
    			this.getBasePriceAsString() +
                this.discountAsString() +
                this.getTransportCostAsString() +
    			this.finalCostAsString();
    }
}
