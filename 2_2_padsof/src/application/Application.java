package application;
import compositePattern.RegisteredCitizen;
import exception.appExceptions.*;

/**
 * The Application class
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */
public class Application {
	public static RegisteredCitizen currentuser = null;
	public static boolean admin = false;
	
	
	public Application() {
	}


	/**
	 * used to login to the application as user or as admin
	 * @param nameorid a string with the name or the id of the user that wants to login
	 * @param password a string with the password
	 * @return true if login was succesfull false otherwise
	 * @throws AlreadyLogInException if its already logged in
	 */
	public static boolean login(String nameorid, String password) throws AlreadyLogInException {
		if(currentuser != null) throw new AlreadyLogInException(currentuser);
		
		if(Admin.checkUser(nameorid, password) != null){
			Application.admin = true;
			return true;
		}
		currentuser = RegisteredCitizen.checkUser(nameorid, password);		
		if (currentuser == null) return false;
		if(currentuser.getBan() == true) {
			currentuser = null;
			return false;
		}
		return true;	
	}
	
	/**
	 * used for logging out of the application
	 * @throws AlreadyLogOutException if app is already logged out
	 */
	public static void logout() throws AlreadyLogOutException {
		if(currentuser == null && admin == false) throw new AlreadyLogOutException();
		currentuser = null;
		admin = false;
	}
	
}
