package ads.assignment3.part6;

/**
 * Home delivered sales class
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 */
public class HomeDeliverySale extends Sale {

    public HomeDeliverySale(Appliance purchased) throws Exception
    {
        super(purchased);
    }

    public HomeDeliverySale(Appliance purchased, Appliance delivered) throws Exception
    {
        super(purchased, delivered);
    }
    
    /**
     * Final Cost of a home delivered sale
     * @return final cost
     */
    public double finalCost()
    {
    	return super.finalCost() + getPurchasedAppliance().transportCost();
    }

    /**
     * Transport Cost of the appliance as a string
     * @return transport cost as string
     */
    public String getTransportCostAsString()
    {
        return "Shipping cost:\t\t" + String.format("%10.2f", getPurchasedAppliance().transportCost()) + "\n";
    }
    
    /**
     * Ticket of the home delivered sale
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
