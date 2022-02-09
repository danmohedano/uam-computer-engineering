package jUnitTesting;

import static org.junit.Assert.*;

import java.util.*;


import org.junit.*;

import compositePattern.Group;
import compositePattern.RegisteredCitizen;
import exception.groupExceptions.*;
import project.*;


public class GroupTest {
	RegisteredCitizen representative;
	RegisteredCitizen member;
	RegisteredCitizen member2;
	RegisteredCitizen member3;
	RegisteredCitizen member4;
	RegisteredCitizen member5;
	RegisteredCitizen member6;

	SocialIssuesProject project1;
	InfrastructureProject project2;
	InfrastructureProject project3;
	SocialIssuesProject project4;
	SocialIssuesProject project5;

	private Group father;
	private Group son;
	private Group son2;
	private Group son3;

	@Before
	public void setUp() throws Exception {
		representative = new RegisteredCitizen("Rick Deckard", "imareplicant", "12345678", false);

		member = new RegisteredCitizen("Rachel Tyrell", "onl", "Nexus-07", false);
		member2 = new RegisteredCitizen("Joe", "impswd", "0KD6-3.7", false);
		member3 = new RegisteredCitizen("Joi", "imnotreal", "0000293D", false);
		member4 = new RegisteredCitizen("Dr. Eldon Tyrell", "replimstrrace", "0000293A", false);
		member5 = new RegisteredCitizen("Dr. Niander Wallace", "replimstrrace", "0000293B", false);

		
		project1 = new SocialIssuesProject("RetireAllReplicants!", "We don't like replicants", 2049.19, member4, "elite", true);
		project2 = new InfrastructureProject("BetterSpinnersforWork!", "We're tired of this bad quality spinners we want faster ones!", 2019.49, representative,"bruh.jpg", null);
		project3 = new InfrastructureProject("BetterBlastersforWork!", "Better Blasters, we're defensless to our enemies with current ones", 2019.49, representative,"bruh.jpg", null);
		project4 = new SocialIssuesProject("SaveReplicants!", "We  like replicants", 2049.19, member4, "elite", true);
		project5 = new SocialIssuesProject("LessPolution!", "We don't like to live in a postapocalitptic world let's change that", 2049.19, member4, "elite", true);

		
		father = new Group("father", representative);
		son = new Group ("son", representative, father);
		son2 = new Group ("son2", representative, father);
		son3 = new Group ("son3", representative, son);

		father.addCitizen(member);
		son.addCitizen(member2);
		son.addCitizen(member3);
		son2.addCitizen(member4);
		
		father.addProject(project2, true);
		son.addProject(project3, true);
		
		father.addProject(project4, false);
		son.addProject(project5, false);
	}
	
	@After
	public void tearDown() {
		Group.setAllGroups(new TreeSet<Group>());
		Project.setAllProjects(new TreeSet<Project>());
		RegisteredCitizen.setAllCitizens(new TreeSet<RegisteredCitizen>());
	}

	@Test
	public void testGetName() {
		assertEquals(father.getName(), "father");
		assertEquals(son.getName(), "son");
	}

	@Test
	public void testGetRepresentative() {
		assertSame(father.getRepresentative(), representative);
		assertSame(son.getRepresentative(), representative);
		
	}

	@Test
	public void testRegisteredCitizenContained() {
		assertTrue(father.RegisteredCitizenContained(member));
		assertFalse(son.RegisteredCitizenContained(member));
		assertTrue(father.RegisteredCitizenContained(member2));
		assertTrue(son.RegisteredCitizenContained(member2));
	}

	@Test
	public void testGetMembers() {
		Set<RegisteredCitizen> allmembers = father.getMembers();
		Set<RegisteredCitizen> subsetmembers = son.getMembers();
		
		assertTrue(allmembers.contains(member));
		assertTrue(allmembers.contains(member2));
		assertTrue(allmembers.contains(member3));
		assertTrue(allmembers.contains(member4));

		assertTrue(subsetmembers.contains(member2));
		assertTrue(subsetmembers.contains(member3));
		
		assertFalse(subsetmembers.contains(member));
		
		
	}

	@Test
	public void testGetFather() {
		assertSame(son.getFather(), father);
		assertNotSame(son.getFather(), son);
	}

	@Test
	public void testGetProjectsSupported() {
		Set<Project> allprojects = father.getProjectsSupported(); //allprojects doesnt really mean that allprojects are included is just to follow variable names
		Set<Project> subset = son.getProjectsSupported();
		
		assertTrue(allprojects.contains(project4));
		assertFalse(allprojects.contains(project5));
		assertFalse(allprojects.contains(project2));
		assertTrue(subset.contains(project5));
		assertTrue(subset.contains(project4));
		assertTrue(subset.contains(project2));
		assertFalse(subset.contains(project3));
	}

	@Test
	public void testGetProjectsCreated() {
		Set<Project> allprojects = father.getProjectsCreated();
		Set<Project> subset = son.getProjectsCreated();
		
		assertTrue(allprojects.contains(project2));
		assertFalse(allprojects.contains(project3));
		assertTrue(subset.contains(project3));
		assertFalse(subset.contains(project2));	}

	@Test (expected = GroupContainsUserException.class)
	public void testAddCitizen() throws Exception {
		RegisteredCitizen bruh = new RegisteredCitizen("bruh", "onl", "Nexus-02", false);
		father.addCitizen(bruh);
		assertTrue(father.RegisteredCitizenContained(bruh));
		father.addCitizen(bruh);
		
		
	}
	
	@Test (expected = Exception.class)
	public void testAddCitizenHierarchy() throws Exception {
		RegisteredCitizen bruh = new RegisteredCitizen("bruh", "onl", "Nexus-01", false);
		father.addCitizen(bruh);
		assertTrue(father.RegisteredCitizenContained(bruh));
		son.addCitizen(bruh);
		
		
	}

	@Test (expected = RemoveRepresentativeException.class)
	public void testRemoveCitizen() throws Exception {
		father.removeCitizen(member);
		assertFalse(father.RegisteredCitizenContained(member));
		father.removeCitizen(representative);
	}

	@Test (expected = Exception.class)
	public void testAddProject() throws Exception {
		father.addProject(project2, false);
	}
	
	@Test (expected = Exception.class)
	public void testAddProjectCreatedNotRepresentative() throws Exception {
		father.addProject(project1, true);
	}

	@Test
	public void testSimilarityReport() throws Exception {
		Group other = new Group("other", representative);
		Project pro = new SocialIssuesProject("hahaha!", "We don't like replicants", 2049.19, representative, "elite", true);
		Project A = new SocialIssuesProject("equipoA!", "We don't like replicants", 2049.19, representative, "elite", true);

		other.addProject(project3, false);
		other.addProject(pro, true);
		other.addProject(A, false);
		son.addProject(pro, false);
		son.addProject(A, true);
		
		assertTrue(other.similarityReport(son) == ((double)3/3));
	}

	@Test
	public void testEqualsObject() {
		assertTrue(father.equals(son.getFather()));
		assertFalse(father.equals(son));
	}

	public void testCompareTo() throws GroupAlreadyExistsException {
		Group testcase = new Group ("esonic", member);
		assertEquals(father.compareTo(son), father.getName().compareTo(son.getName()));
		assertFalse(father.compareTo(son) == father.compareTo(testcase));
	}
	
	@Test (expected = GroupAlreadyExistsException.class)
	public void testCompareToException() throws GroupAlreadyExistsException {
		Group testcase = new Group("father", member);
		assertEquals(father.compareTo(son), father.getName().compareTo(son.getName()));
		assertFalse(father.compareTo(son) == father.compareTo(testcase));
	}
	

	@Test
	public void testGetChildren() {
		Set<Group> allchildren = father.getChildren();
		assertTrue(allchildren.contains(son2));
		assertTrue(allchildren.contains(son));
		assertEquals(allchildren.size(), 2);
	}
	
	public void testGetAllChildren() {
		Set<Group> allchildren = father.getAllChildren();
		assertTrue(allchildren.contains(son2));
		assertTrue(allchildren.contains(son));
		assertTrue(allchildren.contains(son3));
		assertFalse(allchildren.contains(father));

		assertEquals(allchildren.size(), 3);
	}

	@Test
	public void testGetAllGroups() {
		Set<Group> allgroups = Group.getAllGroups();
		assertTrue(allgroups.size() == 4);
		assertTrue(allgroups.contains(father));
		assertTrue(allgroups.contains(son));
		assertTrue(allgroups.contains(son2));
	}

	@Test
	public void testSetAllGroups() {
		SortedSet<Group> allgroups = Group.getAllGroups();
		Group.setAllGroups(null);
		Group.setAllGroups(allgroups);
		allgroups = Group.getAllGroups();
		assertTrue(allgroups.size() == 4);
		assertTrue(allgroups.contains(father));
		assertTrue(allgroups.contains(son));
		assertTrue(allgroups.contains(son2));
	}
	
	@Test
	public void testGetSize() {
		assertTrue(father.getSize() == 5);
		assertTrue(son.getSize() == 3);
		assertTrue(son2.getSize() == 2);

	}
	


}
