package compositePattern;
import java.io.Serializable;
import java.util.*;

import exception.groupExceptions.*;
import project.Project;

/**
 * Group class to handle hierarchy and members of a group
 * @author Rodrigo Juez rodrigo.juezh@estudiante.uam.es
 *
 */
public class Group extends CompositeGroupUser implements Serializable, Comparable<Group>{
	private static final long serialVersionUID = 1L;
	static private SortedSet<Group> allGroups = new TreeSet<>();
	
	private RegisteredCitizen representative;
	private HashSet<RegisteredCitizen> members = new HashSet<>();
	//HashSet are used to caculate quicker the similarity report
	private HashSet<Project> projectsSupported = new HashSet<>(); 
	private HashSet<Project> projectsCreated = new HashSet<>();
	
	private Group father = null;
	private SortedSet <Group> children = new TreeSet<>();
	
	public Group(String name, RegisteredCitizen representative) throws GroupAlreadyExistsException {
		super(name);
		for(Group myGroup: allGroups) 
			if(myGroup.getName().equals(name) == true) {
				throw new GroupAlreadyExistsException(myGroup);
			}
		
		
		this.representative = representative;
		representative.createGroup(this);
		allGroups.add(this);
	}
	

	/**
	 * Creates a group with a father
	 * The father already knows it has this group as children no need to set it
	 * @param name of the group
	 * @param representative of the group
	 * @param father of the group
	 * @throws RepresentativeMatchException if the representative doesnt match
	 * @throws GroupAlreadyExistsException group already exisst
	 */
	public Group(String name, RegisteredCitizen representative, Group father) throws RepresentativeMatchException, GroupAlreadyExistsException {
		super(name);
		for(Group myGroup: allGroups) {
			if(myGroup.getName().equals(name) == true) {
				throw new GroupAlreadyExistsException(myGroup);
			}
		}
		if(representative != father.representative) throw new RepresentativeMatchException(representative, father.representative, name, father.getName());
		this.representative = representative;
		this.father = father;
		father.addChildren(this);
		representative.createGroup(this);
		allGroups.add(this);
	}

	
	/**
	 * Gets group's name
	 * @return group name
	 */
	public String getName() {
		return super.getName();
	}
	
	@Override
	public String toString() {
		if(father != null) 
			return this.getName()+":\n" + 
					"	- Representative: " + this.representative.getName() + "\n" +
					"	- Size: " + this.getSize() + "\n" +
					"	- Father: " + this.father.getName();
		
		return this.getName()+":\n" + 
				"	- Representative: " + this.representative.getName() + "\n" +
				"	- Size: " + this.getSize();
	}
	
	/**
	 * method to obtain the size of the group counting the representative
	 * @return the number of citizens including the representative
	 */
	public int getSize() {
		return getMembers().size() +1;
	}
	
	
	/**
	 * gets group's representative
	 * @return the representative
	 */
	public RegisteredCitizen getRepresentative() {
		return representative;
	}

	/**
	 * is this user contained¿
	 * @param RegisteredCitizen to check if contained
	 * @return True if contained
	 */
	public Boolean RegisteredCitizenContained(RegisteredCitizen RegisteredCitizen) {
		if(members.contains(RegisteredCitizen) == false) {
			for(Group myGroup: this.children) {
				if(myGroup.RegisteredCitizenContained(RegisteredCitizen)) return true;
			}
			
		}
		else return true;
		return false;
		
	}
	
	/**
	 * is it contained directly in the group? not in the children
	 * @param RegisteredCitizen if is directly contained
	 * @return if is contained
	 */
	public Boolean RegisteredCitizenDirectlyContained(RegisteredCitizen RegisteredCitizen) {
		return members.contains(RegisteredCitizen) || this.representative.equals(RegisteredCitizen);
	}
	
	
	
	
	/**
	 * this is used to check if there is a children to the caller group that contains the user, useful to AddCitizen
	 * @param user to check if its contained on children of current groups
	 * @return true if it is
	 */
	private Boolean RegisteredCitizenContainedChildren(RegisteredCitizen user) {
		for(Group myGroup: this.children) {
				if(myGroup.RegisteredCitizenContained(user)) return true;
		}
			
		
		return false;
		
	}
	
	/**
	 * getter of members of this group
	 * @return Set with such members, NOT sorted
	 */
	public Set<RegisteredCitizen> getMembers() {
		Set<RegisteredCitizen> allmembers = new HashSet<>();
		allmembers.addAll(members);
		
		for(Group myGroup: children) {
			allmembers.addAll(myGroup.getMembers());
		}
		
		return allmembers;
	}

	/**
	 * gets group's father
	 * @return gets the members of a group
	 */
	public Group getFather() {
		return father;
	}
	
	/**
	 * gets the projects supported by this group if a project is supported by a child is not supported by the whole group but it is by all the lower level groups
	 * @return list of projects
	 */
	public Set<Project> getProjectsSupported() {
		Set<Project> allsupported = new HashSet<>();
		allsupported.addAll(this.projectsSupported);
		if(father != null) {
			allsupported.addAll(father.getProjectsSupported());
			allsupported.addAll(father.getProjectsCreated());
		}
		return allsupported;
	}
	
	/**
	 * gets the group created by this group
	 * @return list of projects
	 */
	public Set<Project> getProjectsCreated() {
		return projectsCreated;
	}
	
	/**
	 * adds a RegisteredCitizen to the member list
	 * @param user to add
	 * @throws GroupContainsUserException if is contained already
	 */
	public void addCitizen(RegisteredCitizen user) throws GroupContainsUserException  {
		if(members.contains(user) || this.getRepresentative().equals(user)) throw new GroupContainsUserException(user, this);
		if(this.RegisteredCitizenContainedChildren(user)) throw new ChildrenContainsUserException(user, this);
		if(father != null && this.getFather().members.contains(user)) throw new FatherContainsUserException(user, this);
		this.members.add(user);
		user.addGroup(this);
	}
	
	
	
	
	/**
	 * removes a RegisteredCitizen from the citizen list
	 * @param RegisteredCitizen to remove 
	 * @throws RemoveRepresentativeException if tries to remove representative
	 * @throws MemberNotContainedException if not contained
	 * @throws Exception if its contained or its not a member
	 */
	
	/**
	 * removes a RegisteredCitizen from the citizen list
	 * @param RegisteredCitizen to remove 
	 * @throws RemoveRepresentativeException if tries to remove representative
	 * @throws MemberNotContainedException if not contained
	 */
	public void removeCitizen(RegisteredCitizen RegisteredCitizen) throws RemoveRepresentativeException, MemberNotContainedException  {
		if(RegisteredCitizen.equals(representative)) throw new RemoveRepresentativeException(this);
		if(members.contains(RegisteredCitizen)) {
			members.remove(RegisteredCitizen);
			RegisteredCitizen.removeGroup(this);
		}
		else throw new MemberNotContainedException(RegisteredCitizen, this);
		
	}
	
	/**
	 * adds a project supported to the group
	 * @param project to add
	 * @param created True if it was created by the group false if its only supported by it
	 * @throws Exception is project is already added, if representatives dont match
	 */
	public void addProject(Project project, Boolean created) throws Exception { //no need to check if it is already in one of the sons because as they're sets it wont be repeated
		if(this.getProjectsCreated().contains(project) || this.getProjectsSupported().contains(project)) throw new ProjectAlreadyAddedException(project, this);

		if(created == true) {
			if(project.getCreator() != this.getRepresentative()) throw new RepresentativeMatchException(project.getCreator(), this.getRepresentative(), project.getName(), this.getName());
			projectsCreated.add(project);
		}
		else {
			projectsSupported.add(project);
		}
	}
	
	/**
	 * ads a children to this group	
	 * @param child to add
	 */
	private void addChildren(Group child) {
		if(children.contains(child)) return;
		children.add(child);
	}
	
	/**
	 * Request the similarity report between two groups
	 * @param other the second group of the similarity report
	 * @return score of the similarity report
	 */
	public double similarityReport(Group other){
		
		double n = this.projectsCreated.size() +  other.projectsCreated.size();
		double n1 = IntersectionSize(this.projectsCreated, other.getProjectsSupported());
		double n2 = IntersectionSize(this.projectsSupported, other.getProjectsCreated());
		return (n1+n2)/n;
	}
	
	
	
	/**
	 * 
	 * @param first set to intersect
	 * @param second set to intersect
	 * @return the Intersection of two Lists
	 */
	private static Set<Project> Intersect(Set<Project> first, Set<Project> second) {
		HashSet<Project> intersection = new HashSet<>(); 
	     
	    intersection.addAll(first);
	     
	    intersection.retainAll(second);			
		
		return new HashSet<Project>(intersection);		
	}
	
	/**
	 * 
	 * @param first to know the intersection size
	 * @param second to know the intersection size
	 * @return with size
	 */
	private static int IntersectionSize(Set<Project> first, Set<Project> second) {
		return Intersect(first,second).size();
	}
	
	@Override
    public boolean equals(Object other) {
		if(other == null || other.getClass() != this.getClass()) return false;
		
		return super.getName().equals(((Group)other).getName());
		
    }
	

	/**
	 * based on name comparison
	 * @param other group to compare
	 * @return integer with comparison
	 */
	public int compareTo(Group other) {
		return this.getName().compareTo(other.getName());
	}

	
	/**
	 * gets the subgroups of current group
	 * @return with direct children
	 */
	public SortedSet<Group> getChildren() {
		return children;
	}
	
	/**
	 * gets all children including granchildren and so on
	 * @return all children
	 */
	public SortedSet<Group> getAllChildren(){
		SortedSet<Group> allchildren = new TreeSet<>();
		allchildren.addAll(children);
		SortedSet<Group> temp = new TreeSet<>();

		for(Group myGroup: children) 
			if((temp = myGroup.getAllChildren()) != null)
				allchildren.addAll(temp);
		return allchildren;		
	}
	/**
	 * used for storing persistent data
	 * @return all groups in the application
	 */
	public static SortedSet<Group> getAllGroups() {
		return allGroups;
	}
	
	/**
	 * used for persistance purposes
	 * @param set with all the projects
	 */
	public static void setAllGroups(SortedSet<Group> set)
	{
		Group.allGroups = set;
	}
	@Override
	public int hashCode() {
		if(super.getName() == null) return super.hashCode();
		return super.getName().hashCode();
    }
	
	
	/**
	 * searchs a group based on a string
	 * @param contains if contains this string returned in collection
	 * @return collection with results
	 */
	public static List<String> GroupSearch(String contains){
		ArrayList<String> result = new ArrayList<>();
		System.out.println(contains);
		for(Group myGroup: Group.getAllGroups()) {
			for(int i=0; i<myGroup.getName().length()-contains.length()+2; i+=1) {
				if(myGroup.getName().startsWith(contains, i) == true) {
					result.add(myGroup.getName());
					break;
				}
			}
		}
		return result;
	}
	
	/**
	 * gets group based on name
	 * @param name of group to get
	 * @return Group requested or null if it wasn't found
	 */
	public static Group getGroup(String name) {
		for(Group myGroup: Group.getAllGroups()) {
			if(myGroup.getName().compareTo(name) == 0) {
				return myGroup;
			}
		}
		return null;
	}


	@Override
	public Collection<CompositeGroupUser> getUsers() {
		ArrayList<CompositeGroupUser> returnvalue = new ArrayList<>();
		returnvalue.addAll(members);
		for(CompositeGroupUser myChild: children) {
			returnvalue.addAll(myChild.getUsers()); /*base case of recursion: we find a user and it returns itself instead of iterate more*/
		}
		return returnvalue;
	}
	
	
	
}
