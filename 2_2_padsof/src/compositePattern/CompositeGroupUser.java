package compositePattern;

import java.io.Serializable;
import java.util.Collection;


/**
 * CompositeGroupUser class to handle hierarchy and members of groups and users
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */
public abstract class CompositeGroupUser implements Serializable {
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private String name; //Name of the user
	
	
	public CompositeGroupUser(String name) {
		this.name = name;
	}
	
	public abstract Collection<CompositeGroupUser> getUsers();
	
	/**
	 * @return name -the name
	 */
	public String getName() {
		return name;
	}


	/**
	 * @param name -the name to set
	 */
	public void setName(String name) {
		this.name = name;
	}

}
