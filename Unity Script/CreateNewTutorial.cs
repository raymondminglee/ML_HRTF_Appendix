using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Oculus.Platform;

public class CreateNewTutorial : MonoBehaviour
{
    public Transform Speaker;
    //GameObject Speakerclone;

    // number of azimuth from 1 to 25
    public int azn; 
    // number of elevation from 1 to 50
    public int eln;
    // raduis
    public int r;

    // create 

    int c = 0;

    // for height 
    public int height;

    // Use this for initialization

    int[] azimuth = { -80, - 65, -55, -45, -40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10,15, 20, 25, 30, 35, 40, 45, 55, 65, 80};
    float[] elevation = new float[50];

    void Start()
    {
        for (int i = 0; i<50; i++)
        {
            elevation[i] = -45 + (float)5.625 * i;
        }

        // instantiate new game object speaker
        for (int j = 0; j < azn; j++)
        {
            for (int k = 0; k < eln; k++)
            {
                float X_1 = r * Mathf.Sin(azimuth[j] * Mathf.PI / 180);
                float X_2 = r * Mathf.Cos(azimuth[j] * Mathf.PI / 180) * Mathf.Cos(elevation[k] * Mathf.PI / 180);
                float X_3 = r * Mathf.Cos(azimuth[j] * Mathf.PI / 180) * Mathf.Sin(elevation[k] * Mathf.PI / 180) + height;
                //Speakerclone = Instantiate(Speaker, new Vector3(X_1, X_3, X_2), Quaternion.identity) as GameObject;
                Instantiate(Speaker, new Vector3(X_1, X_3, X_2), Quaternion.identity);
            }
        }
    }

    // Update is called once per frame




/*
    private void OnGUI()
    {
        if(GUI.Button(new Rect(20, Screen.height * 0.66f, 200, 30), "Initialize Virtual Speaker"))
        {
            CreateClones();
        }

    }
    */
}
