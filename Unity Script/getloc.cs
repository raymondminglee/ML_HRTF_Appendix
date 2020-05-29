using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class getloc : MonoBehaviour {

    public GameObject GSphere;

    int ispush;
    public int Subjectnum;
	// Use this for initialization
    void CreateText()
    {
        string path = Application.dataPath + "/Log_Sub_" + Subjectnum+ ".txt";
        if (!File.Exists(path))
        {
            File.WriteAllText(path, "Login log \n\n");
        }
    }

    void Writetext()
    {
        string path = Application.dataPath + "/Log_Sub_" + Subjectnum + ".txt";
        string content = "Login date" + System.DateTime.Now + "\n" + "Location" + GSphere.transform.position + "\n";
        File.AppendAllText(path, content);
    }
	void Start () {
        CreateText();
        ispush = 0;
	}
	
	// Update is called once per frame
	void Update () {
		if (OVRInput.Get(OVRInput.Button.PrimaryIndexTrigger) == true && ispush == 0)
        {
            print(GSphere.transform.position);
            print(ispush);
            Debug.Log("Button One Pressed");
            ispush = 1;
            print(ispush);
            Writetext();
        }
        if (OVRInput.Get(OVRInput.Button.PrimaryIndexTrigger) == false && ispush == 1)
        {
            ispush = 0;
			print(GSphere.transform.position);
            print(ispush);

        }
        
	}
}
