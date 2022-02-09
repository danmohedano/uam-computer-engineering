/**
 * 
 */
package application;
import java.util.Collection;

import compositePattern.CompositeGroupUser;
import compositePattern.RegisteredCitizen;
import compositePattern.User;
import exception.projectExceptions.InvalidThresholdProjectException;
import project.*;

/**
 * Admin class
 * @author Silvia Sopeña silvia.sopenna@estudiante.uam.es
 *
 */
public class Admin extends User
	{ 
	private static final long serialVersionUID = 1L;
	private static Admin admin;	
	
	/**
	 * Constructor of the admin class
	 * @param name -name of the admin
	 * @param pwd -password of the admin
	 */
	private Admin(String name, String pwd) 
	{
		
		super(name, pwd);	
		
	}
	
	/**
	 * Singleton for the admin
	 * @return admin -the admin
	 */
	public static Admin getAdmin()
	{
		if(admin == null) 
		{
			admin = new Admin("admin", "admin");
			return admin;
		}
		return admin;
	}
	
	
	
	/**
	 * method to validate the project and set it accepted or not
	 * @param p -the project
	 * @param accept -accepted or not
	 * @param reason -reason
	 * @return bool -true if the project is validated
	 */
	public static boolean validate(Project p, boolean accept, String reason) 
	{
		if(p.getStatus() == Status.CREATED)
		{
			if (accept == true) {
			p.setStatus(Status.ONGOING);
			p.notifyAll(Status.ONGOING);
			return true;
			}
			else 
			{
				p.setStatus(Status.REJECTED);
				p.setRejectionReason(reason);
				p.notifyAll(Status.REJECTED, reason);
				return true;
			}
		}
		else
		{
			return false;
		}
	}
	
	
	/**
	 * method to set the threshold
	 * @param n -number of the threshold
	 * @throws InvalidThresholdProjectException -The exception
	 */
	public static void setThreshold(int n) throws InvalidThresholdProjectException 
	{
		Project.setThreshold(n);
	}
	
	/**
	 * method for checking  if the user is an admin or not
	 * @param text -name
	 * @param pwd -password
	 * @return admin -the admin if it exists and null if not
	 */
	public static Admin checkUser(String text, String pwd) 
	{
		if(getAdmin().getName().equals(text) && admin.getPwd().equals(pwd)) return admin;
		
		return null;
	}
	
	/**
	 * method to accept or reject the new user
	 * @param c -the citizen to accept
	 */	
	public static void acceptCitizen(RegisteredCitizen c) 
	{
		if(RegisteredCitizen.getNewCitizens().contains(c) == true) 
		{		
			RegisteredCitizen.removeNewCitizens(c);
		}
	}
	
	
	
	
	public String toString() 
	{
		return "Administrator:" + this.getName() + "\n";	
	}

	@Override
	public Collection<CompositeGroupUser> getUsers() {
		return null;
	}
	
	

	

}
