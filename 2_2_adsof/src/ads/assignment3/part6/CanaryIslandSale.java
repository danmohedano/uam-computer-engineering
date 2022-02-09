/**
 * 
 */
package ads.assignment3.part6;

/**
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 *
 */
public class CanaryIslandSale extends Sale {

	public CanaryIslandSale(Appliance purchased) throws Exception
	{
		super(purchased);
	}
	
	public CanaryIslandSale(Appliance purchased, Appliance delivered) throws Exception
	{
		super(purchased, delivered);
	}		
}
