package jUnitTesting;

import static org.junit.Assert.*;

import java.util.Set;

import org.junit.Before;
import org.junit.Test;

import compositePattern.Group;
import compositePattern.RegisteredCitizen;
import persistence.Persistence;
import project.InfrastructureProject;
import project.Project;
import project.SocialIssuesProject;

public class PersistenceTest {

	RegisteredCitizen representative;
	RegisteredCitizen member;
	RegisteredCitizen member2;
	RegisteredCitizen member3;
	RegisteredCitizen member4;
	
	SocialIssuesProject project1;
	InfrastructureProject project2;
	InfrastructureProject project3;
	SocialIssuesProject project4;
	SocialIssuesProject project5;

	private Group father;
	private Group son;
	private Group son2;
	
	@Before
	public void setUp() throws Exception {
		representative = new RegisteredCitizen("Rick Deckard", "imareplicant", "12345678", false);

		member = new RegisteredCitizen("Rachel Tyrell", "onl", "Nexus-07", false);
		member2 = new RegisteredCitizen("Joe", "impswd", "0KD6-3.7", false);
		member3 = new RegisteredCitizen("Joi", "imnotreal", "0000293D", false);
		member4 = new RegisteredCitizen("Dr. Eldon Tyrell", "replimstrrace", "0000293A", false);

		project1 = new SocialIssuesProject("RetireAllReplicants!", "We don't like replicants", 2049.19, member4, "elite", true);
		project2 = new InfrastructureProject("BetterSpinnersforWork!", "We're tired of this bad quality spinners we want faster ones!", 2019.49, representative,"bruh.jpg", null);
		project3 = new InfrastructureProject("BetterBlastersforWork!", "Better Blasters, we're defensless to our enemies with current ones", 2019.49, representative,"bruh.jpg", null);
		project4 = new SocialIssuesProject("SaveReplicants!", "We  like replicants", 2049.19, member4, "elite", true);
		project5 = new SocialIssuesProject("LessPolution!", "We don't like to live in a postapocalitptic world let's change that", 2049.19, member4, "elite", true);

		
		father = new Group("father", representative);
		son = new Group ("son", representative, father);
		son2 = new Group ("son2", representative, father);

		father.addCitizen(member);
		son.addCitizen(member2);
		son.addCitizen(member3);
		son2.addCitizen(member4);
		
		father.addProject(project2, true);
		son.addProject(project3, true);
		
		father.addProject(project4, false);
		son.addProject(project5, false);
	}

	
	@Test
	public void ReadandWrite() {
		Persistence.saveAll();
		
		RegisteredCitizen.setAllCitizens(null);
		Group.setAllGroups(null);
		Project.setAllProjects(null);
	
		Persistence.readAll();
		Set<Project> allprojects = Project.getAllProjects();
		Set<Group> allgroups = Group.getAllGroups();
		Set<RegisteredCitizen> allusers = RegisteredCitizen.getAllCitizens();

		assertTrue(allprojects.size() == 5);
		assertTrue(allgroups.size() == 3);
		assertTrue(allusers.size() == 5);
		
		assertTrue(allprojects.contains(project1));
		assertTrue(allprojects.contains(project2));
		assertTrue(allprojects.contains(project3));
		assertTrue(allprojects.contains(project4));
		assertTrue(allprojects.contains(project5));

		assertTrue(allgroups.contains(father));
		assertTrue(allgroups.contains(son));
		assertTrue(allgroups.contains(son2));
		
		assertTrue(allusers.contains(representative));
		assertTrue(allusers.contains(member));
		assertTrue(allusers.contains(member2));
		assertTrue(allusers.contains(member3));
		assertTrue(allusers.contains(member4));


	}
	

}
