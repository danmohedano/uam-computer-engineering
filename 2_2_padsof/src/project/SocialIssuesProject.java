/**
 * 
 */
package project;


import compositePattern.Group;
import compositePattern.RegisteredCitizen;
import exception.projectExceptions.InvalidInfoProjectException;
import exception.projectExceptions.PreExistingProjectException;


/**
 * Social Issues Project Class
 * @author Daniel Mohedano daniel.mohedano@estudiante.uam.es
 *
 */
public class SocialIssuesProject extends Project {
	private static final long serialVersionUID = 1L;
	private String socialGroup; //Social group that the project will affect
	private boolean aim; //Aim of the project. False: national True: international
	
	
	public SocialIssuesProject(String name, String description, double money, RegisteredCitizen creator, String socialGroup, boolean aim)  throws Exception
	{
		super(name, description, money, creator);
		this.socialGroup = socialGroup;
		this.aim = aim;
	}
	
	public SocialIssuesProject(String name, String description, double money, RegisteredCitizen creator, Group group, String socialGroup, boolean aim)  throws InvalidInfoProjectException, PreExistingProjectException, Exception
	{
		super(name, description, money, creator, group);
		this.socialGroup = socialGroup;
		this.aim = aim;
	}

	@Override
	public String getExtraData() {
		String extraData = this.socialGroup + ", " + aim;
		return extraData;
	}

	@Override
	public ProjectKind getProjectKind() {
		return ProjectKind.Social;
	}
	
	public String toString() {
		return "(SI) " + super.toString();
	}

	/**
	 * @return the socialGroup
	 */
	public String getSocialGroup() {
		return socialGroup;
	}

	/**
	 * @param socialGroup the socialGroup to set
	 */
	public void setSocialGroup(String socialGroup) {
		this.socialGroup = socialGroup;
	}

	/**
	 * @return the aim
	 */
	public boolean isAim() {
		return aim;
	}

	/**
	 * @param aim the aim to set
	 */
	public void setAim(boolean aim) {
		this.aim = aim;
	}
}
