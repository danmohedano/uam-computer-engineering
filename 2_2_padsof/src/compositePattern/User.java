/**
 * 
 */
package compositePattern;

import java.io.Serializable;

/**
 * User Class
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 *
 */
public abstract class User extends CompositeGroupUser implements Serializable 
	{
	
	private static final long serialVersionUID = 1L;
	private String pwd; //Password of the user
	
	
	/**
	 * Constructor of the User class
	 * @param name -users name
	 * @param pwd -users password
	 */
	public User(String name, String pwd) 
	{
		super(name);
		this.pwd = pwd; 
		
	}
	


	/**
	 * @return pwd -the pwd
	 */
	public String getPwd() {
		return pwd;
	}


	/**
	 * 
	 * @param pwd -password
	 */
	public void setPwd(String pwd) {
		this.pwd = pwd;
	}
	
	

			
	public String toString()
	{
		return "User:" + this.getName() + "\n";
	}

}
