package ads.assignment3;

import java.util.List;

/**
 * Television class
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 */
public class Television extends Appliance{
    private double screenSize;

    public Television(String brand, String model, double basePrice, EnergyEfficiency efficiency, double screenSize)
    {
        super(brand, model, basePrice, efficiency);
        this.screenSize = screenSize;
    }

    public Television(List<String> data)
    {
		this(data.get(0), data.get(1), Double.parseDouble(data.get(2)), EnergyEfficiency.valueOf(data.get(3)), Double.parseDouble(data.get(4)));
	}

	/**
     * Method to calculate the transport cost of the television
     * @return transport cost
     */
    public double transportCost()
    {
        double cost;
        if (screenSize <= 40)
        {
            if (super.getBasePrice() > 500) cost = 0;
            else cost = 35;
        }
        else
        {
            cost = 35 + (screenSize - 40);
        }
        return cost;
    }
    
    /**
     * Checks if the arguments are valid to create an Television
     * @param data - arguments
     * @return true if arguments are valid
     */
    public static boolean check(List<String> data)
    {
    	try {	Double.parseDouble(data.get(4));}
    	catch(NumberFormatException e) {return false;}
    	
    	if (Double.parseDouble(data.get(4)) <= 0) return false;
    	
    	return Appliance.check(data);
    }
}
