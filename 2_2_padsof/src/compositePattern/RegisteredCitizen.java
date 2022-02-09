/**
 * 
 */
package compositePattern;

import project.*;
import notification.Notification;

import java.util.*;


/**
 * RegisteredCitizen class
 * @author Silvia Sope�a silvia.sopenna@estudiante.uam.es
 *
 */
public class RegisteredCitizen extends User implements Comparable<RegisteredCitizen> 
{
	private static final long serialVersionUID = 1L;
	private String id; //This is the id of the registered citizen	
	private boolean ban; //boolean that indicates if the user is banned or not
	
	private static SortedSet<RegisteredCitizen> allCitizens= new TreeSet<>(); //HashSet of all the users registered in the application
	
	private HashSet<Group> groupsJoined = new HashSet<>(); //HashSet of groups the user belongs to
	private HashSet<Group> groupsRepresented = new HashSet<>(); //HashSet of the groups the user represents
	
	private HashSet<Project> projectsCreated= new HashSet<>(); //HashSet of the projects created by the user
	private HashSet<Project> projectsVoted= new HashSet<>(); //HashSet of the projects voted by the user
	private HashSet<Project> projectsSubscribed= new HashSet<>(); //HashSet of the projects the user is subscribed to
	
	private List<Notification> notifications = new ArrayList<>(); //List with all the notifications	
	private boolean newly = true;
	
	/**
	 * Constructor of the class Registered Citizen
	 * @param name -name of the citizen
	 * @param pwd -password
	 * @param id -id
	 * @param ban -banned or not
	 * @throws Exception -the exception
	 */
	public RegisteredCitizen(String name, String pwd, String id, boolean ban) throws Exception
	{
		super(name, pwd);
		this.id = id;
		this.ban = false;
		//TODO value for error and 
		if(id.length() != 8)   throw new Exception("Invalid id");
		if(allCitizens.contains(this) == true) throw new Exception("Already in system");
		else
		{
			allCitizens.add(this);

		}
		
	}
	@Override
	public boolean equals(Object obj) 
	{
		if (obj == null || obj.getClass() != this.getClass()) return false;
		return ((RegisteredCitizen)obj).getName().equals(this.getName()) || ((RegisteredCitizen)obj).id.equals(this.id);
	}
	
	/**
	 * @return groupsJoined -the groupsJoined
	 */
	public HashSet<Group> getGroupsJoined() {
		return groupsJoined;
	}
	/**
	 * @return groupsRepresented -the groupsRepresented
	 */
	public HashSet<Group> getGroupsRepresented() {
		return groupsRepresented;
	}
	/**
	 * @return projectsCreated -the projectsCreated
	 */
	public HashSet<Project> getProjectsCreated() {
		return projectsCreated;
	}
	/**
	 * @return projectsVoted -the projectsVoted
	 */
	public HashSet<Project> getProjectsVoted() {
		return projectsVoted;
	}
	/**
	 * @return projectsSubscribed -the projectsSubscribed
	 */
	public HashSet<Project> getProjectsSubscribed() {
		return projectsSubscribed;
	}
	
	@Override 
	public int hashCode()
	{
		if(getName() == null || this.id == null) return super.hashCode();
		return getName().hashCode() * id.hashCode();
	}
	
	
	public int compareTo(RegisteredCitizen c) {
		if(this.getName().compareTo(c.getName()) == 0) return 0;
		else if(id.compareTo(c.id) == 0) return 0;
		return getName().compareTo(c.getName());
	}
	
	
	/**
	 * @return the id -id we want to get
	 */
	public String getId() {
		return id;
	}

	/**
	 * @param id -id we want to set
	 */
	public void setId(String id) {
		this.id = id;
	}
	

	/**
	 * method Updates notifications if the citizen is subscribed
	 * @param p -project to update
	 * @param status -status of the project
	 */
	public void update(Project p, Status status) 
	{
		notifications.add(new Notification(p, status));
	}
	
	/**
	 * method Updates notifications if the citizen is subscribed with a given reason
	 * @param p -project to update
	 * @param status -status of the project
	 * @param reason -reason 
	 */
	public void update(Project p, Status status, String reason) {
		notifications.add(new Notification(p, status, reason));
	}
	
	/**
	 * @return the list of notifications
	 */
	public List<Notification> getNotification() 
	{
		return notifications;
	}
	
	/**
	 * @return the list of notifications read
	 */
	public boolean getReadNotification() 
	{
		for(Notification n: notifications) {
			if(n.isRead() == false) return true;
		}
		return false;
	}
	
	/**
	 * method for creating a group
	 * @param g -the group
	 */
	public void createGroup(Group g) 
	{
		groupsRepresented.add(g);
	}
	
	/**
	 * method for joining a group (used by group only)
	 * @param g -the group
	 */
	public void addGroup(Group g)
	{
		groupsJoined.add(g);
	}
	
	/**
	 * method for leaving a group (used by group only)
	 * @param g -the group
	 */
	public void removeGroup(Group g)
	{
		groupsJoined.remove(g);
	}
	
	/**
	 * method for voting a project as a citizen
	 * @param p -the project
	 */
	public void vote(Project p)
	{
		projectsVoted.add(p);
	}
	
	
	/**
	 * method for subscribing to a project
	 * @param p -the project
	 */
	public void subscribe(Project p)
	{
		projectsSubscribed.add(p);
	}
	
	/**
	 * method for unsubscribe from a project
	 * @param p -the project
	 */
	public void unsubscribe(Project p)
	{
		projectsSubscribed.remove(p);
	}
	
	
	/**
	 * method for creating project
	 * @param p -the project
	 */
	public void createProject(Project p)
	{
		projectsCreated.add(p);
	}
	
	
	/**
	 * method for checking  if the user is registered or not
	 * @param text -the name
	 * @param pwd -the password
	 * @return i -true if the user is registered and false if it's not
	 */
	public static RegisteredCitizen checkUser(String text, String pwd) 
	{
		for(RegisteredCitizen i: allCitizens)
		{
			if(i.getPwd().equals(pwd) && ((i.getName().equals(text) || i.id.equals(text))))
			{
				if(i.newly == true) return null;
				return i;
			}
		}
		return null;

	}
	
	
	/**
	 * method for setting all Citizens
	 * @param set -set of all the citizens
	 */
	public static void setAllCitizens(SortedSet<RegisteredCitizen> set) 
	{
		RegisteredCitizen.allCitizens = set;
	}

	
	
	/**
	 * @return allCitizens -all the citizens
	 */
	public static SortedSet<RegisteredCitizen> getAllCitizens() {
		return allCitizens;
	}
	
	/**
	 * @return allCitizens -all the new citizens
	 */
	public static SortedSet<RegisteredCitizen> getNewCitizens() {
		SortedSet<RegisteredCitizen> news = new TreeSet<>();
		for(RegisteredCitizen myCit: RegisteredCitizen.getAllCitizens()) {
			if(myCit.newly == true) {
				news.add(myCit);
			}
		}
		return news;
	}
	
	/**
	 * method for removing a citizen from the newCitizens set
	 * @param c the citizen to remove
	 */
	public static void removeNewCitizens(RegisteredCitizen c) {
		c.newly= false;
	}
	

	/**
	 * method for banning a user
	 */
	public void banUser() 
	{
		ban =!ban;
	}
	

	/**
	 * gets the ban
	 * @return ban -the ban
	 */
	public boolean getBan() 
	{
		return ban;
	}


	/**
	 * sets the ban
	 * @param ban -the ban to set
	 */
	public void setBan(boolean ban) 
	{
		this.ban = ban;
	}

	/**
	 * checks if the group given is represented by the citizen
	 * @param g -the group
	 * @return g -true if the group given is represented by the citizen
	 */
	public boolean checkRepresentedGroup(Group g) 
	{
		return groupsRepresented.contains(g);

	}
	
	/**
	 * checks if the project given is created by the citizen
	 * @param p -the project
	 * @return p -true if the project is created by the citizen
	 */
	public boolean checkCreatedProject(Project p) 
	{
		return projectsCreated.contains(p);

	}
	
	/**
	 * checks if the project given is voted by the citizen
	 * @param p -the project
	 * @return p -true if the project given is voted by the citizen
	 */
	public boolean checkVotedProject(Project p) 
	{
		return projectsVoted.contains(p);

	}
	
	/**
	 * checks if the citizen is subscribed to the project given as argument
	 * @param p -the project
	 * @return p -true if the citizen is subscribed to the project given as argument
	 */
	public boolean checkSubscribedProject(Project p) 
	{
		return projectsSubscribed.contains(p);

	}
	
	
	/**
	 * checks if the user has joined the group given as argument
	 * @param g -the group
	 * @return g -true if the user has joined the group given as argument
	 */
	public boolean checkJoinedGroup(Group g) 
	{
		return groupsJoined.contains(g);

	}
	
	/**
	 * gets the citizen given its name
	 * @param n -the name
	 * @return c -the citizen
	 */
	public static RegisteredCitizen getCitizenByName(String n) 
	{

		for(RegisteredCitizen c: allCitizens) {
			if(c.getName().compareTo(n) == 0)
				return c;
		}
		
		return null;

	}
	

	public String toString()		{
		return this.getName() + ":\n	- ID: " + this.getId() + "\n" + "	- Banned: " + this.getBan();
	}
	@Override
	public Collection<CompositeGroupUser> getUsers() {
		Collection<CompositeGroupUser> returnvalue  = new ArrayList<CompositeGroupUser>();
		if(this.ban == true) return returnvalue;
		returnvalue.add(this);
		return returnvalue;
	}	
	
}
