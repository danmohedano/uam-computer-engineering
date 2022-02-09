package ads.assignment3.part6;

/**
 * Dimension class to store dimensions of appliances
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 */
public class Dimension {
    private double x;
    private double y;
    private double z;

    public Dimension(double x, double y, double z){
        this.x = x;
        this.y = y;
        this.z = z;
    }

	public Dimension(String x, String y, String z) {
		this(Double.parseDouble(x), Double.parseDouble(y), Double.parseDouble(z));
	}

	/**
	 * Calculates the volume of the dimensions
	 * @return the volume
	 */
	public double volume()
	{
		return x*y*z/1000000;
	}
	
	/**
	 * @return the x
	 */
	public double getX() {
		return x;
	}

	/**
	 * @param x the x to set
	 */
	public void setX(double x) {
		this.x = x;
	}

	/**
	 * @return the y
	 */
	public double getY() {
		return y;
	}

	/**
	 * @param y the y to set
	 */
	public void setY(double y) {
		this.y = y;
	}

	/**
	 * @return the z
	 */
	public double getZ() {
		return z;
	}

	/**
	 * @param z the z to set
	 */
	public void setZ(double z) {
		this.z = z;
	}
}
