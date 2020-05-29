/************************************************************************************

Copyright   :   Copyright 2017-Present Oculus VR, LLC. All Rights reserved.

Licensed under the Oculus VR Rift SDK License Version 3.2 (the "License");
you may not use the Oculus VR Rift SDK except in compliance with the License,
which is provided at the time of installation or download, or which
otherwise accompanies this software in either electronic or hard copy form.

You may obtain a copy of the License at

http://www.oculusvr.com/licenses/LICENSE-3.2

Unless required by applicable law or agreed to in writing, the Oculus VR SDK
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

************************************************************************************/

using System;
using System.IO;
using UnityEngine;
using UnityEngine.SceneManagement;


public class LocalizationInteraction : MonoBehaviour {
    static int trial_num = 0;
    private int ispush;
    private int ispush_2;

    public Material Next_idle;
    public Material Next_active;
    public Material Play_idle;
    public Material Play_active;
    public Material Finish_idle;
    public Material Finish_active;
    public Material Red;
    public Material Green;

    public GameObject Play_button;
    public GameObject Next_button;
    public GameObject Finish_button;
    public GameObject Visualizer;

    public GameObject GSphere;
    public GameObject EyeCenter;

    private AudioSource stimuli;
    private string intpos;
    private string introt;
    public int Subjectnum;
    public int audio_id; //0 speech, 1 noise, 2 music
    public int set_id; // 0 generic 1 extimate

    private string content;

    String[] stimuli_name_train = new string[] { "t4", "t2", "t1", "t3" };
    String[] audio_id_name = new string[] { "speech", "noise", "music" };
    String[] set_id_name = new string[] { "generic", "est" };
    String [] stimuli_name = new string[] { "3", "2", "1", "1", "5", "2", "3", "2", "3", "4", "5", "5", "3", "4", "2", "1", "4", "5", "1", "4" };

    void CreateText()
    {
        string path = Application.dataPath + "Subject" + Subjectnum + "_"+ set_id_name[set_id] + "_" + audio_id_name[audio_id] + ".txt";
        if (!File.Exists(path))
        {
            print("writing haed");
            //File.WriteAllText(path, "Login log \n\n");
            Writehead();
        }
    }

    void Writehead()
    {
        string path = Application.dataPath + "Subject" + Subjectnum + "_" + set_id_name[set_id] + "_" + audio_id_name[audio_id] + ".txt";
        string head = "Login date" + ";" + "Stimuli Location" + ";" + "Head Position" + ";" + "Head Rotation" + ";" + "Point Location" + "\n";
        File.AppendAllText(path, head);
    }

    void Writetext(string content)
    {
        string path = Application.dataPath + "Subject" + Subjectnum + "_" + set_id_name[set_id] + "_" + audio_id_name[audio_id] + ".txt";
        //string content = System.DateTime.Now + ";" + stimuli_name[trial_num-stimuli_name_train.Length].ToString() + ";" + intpos + ";" + introt + ";" + GSphere.transform.position + "\n";
        File.AppendAllText(path, content);
    }

    void Start () {
        CreateText();
        ispush = 0;
        ispush_2 = 0;
        Vector3 eye_center = EyeCenter.transform.position;
        //Play_button.transform.position = new Vector3(Convert.ToSingle(20*Math.Sin(Convert.ToDouble(EyeCenter.transform.eulerAngles.y)*Math.PI/180)), Play_button.transform.position.y, Convert.ToSingle(20 * Math.Cos(Convert.ToDouble(EyeCenter.transform.eulerAngles.y) * Math.PI / 180)));
        //Play_button.transform.eulerAngles = new Vector3(Play_button.transform.eulerAngles.x, EyeCenter.transform.eulerAngles.y, Play_button.transform.eulerAngles.z);
        Play_button.transform.position = new Vector3(Convert.ToSingle(20 * Math.Sin(Convert.ToDouble(EyeCenter.transform.eulerAngles.y) * Math.PI / 180)), Play_button.transform.position.y, Convert.ToSingle(20 * Math.Cos(Convert.ToDouble(EyeCenter.transform.eulerAngles.y) * Math.PI / 180)));
        Play_button.transform.eulerAngles = new Vector3(Play_button.transform.eulerAngles.x, EyeCenter.transform.eulerAngles.y, Play_button.transform.eulerAngles.z);
        //Play_button.transform.position = Next_button.transform.position;
        //Play_button.transform.eulerAngles = Next_button.transform.eulerAngles;
        Next_button.SetActive(false);
        Finish_button.SetActive(false);

        if (trial_num == stimuli_name.Length + stimuli_name_train.Length){
            Play_button.SetActive(false);
            Next_button.SetActive(false);
            Finish_button.transform.position = Next_button.transform.position;
            Finish_button.transform.eulerAngles = Next_button.transform.eulerAngles;
            Finish_button.SetActive(true);
        } 
    }

	public void OnHoverEnter(Transform t) {
        if (t.gameObject.name == "Next_button") {
            t.gameObject.GetComponent<Renderer>().material = Next_active;
        }
		if (t.gameObject.name == "Play_button") {
            t.gameObject.GetComponent<Renderer>().material = Play_active;
        }
        if (t.gameObject.name == "Finish_button")
        {
            t.gameObject.GetComponent<Renderer>().material = Finish_active;
        }
    }

    public void OnHoverExit(Transform t) {
        if (t.gameObject.name == "Next_button") {
            t.gameObject.GetComponent<Renderer>().material = Next_idle;
        }
		if (t.gameObject.name == "Play_button"){
			t.gameObject.GetComponent<Renderer>().material = Play_idle;
		}
        if (t.gameObject.name == "Finish_button")
        {
            t.gameObject.GetComponent<Renderer>().material = Finish_idle;
        }
    }

	public void OnSelected (Transform t){
		if (t.gameObject.name == "Next_button"){
		    trial_num += 1;
            //print(trial_num);
            print(content);
            Writetext(content);
            SceneManager.LoadScene(SceneManager.GetActiveScene().name);
		// refreash
		}
		if (t.gameObject.name == "Play_button"){
			Play_button.SetActive(false);
			Next_button.SetActive(false);
            //string audio_path = Application.dataPath + "/Log_Sub_" + Subjectnum + ".txt";
            print("trial num is"+trial_num);
            print(audio_id_name[audio_id] + "_" + set_id_name[set_id]);
            if (trial_num < stimuli_name_train.Length)
            {
                stimuli = GetComponent<AudioSource>();
                stimuli.clip = Resources.Load<AudioClip>(stimuli_name_train[trial_num]+"_"+ audio_id_name[audio_id] + "_"+ set_id_name[set_id]);
                print("playing");
                stimuli.Play();
            }
            else
            {
                stimuli = GetComponent<AudioSource>();
                stimuli.clip = Resources.Load<AudioClip>(stimuli_name[trial_num-stimuli_name_train.Length] + "_" + audio_id_name[audio_id] + "_" + set_id_name[set_id]);
                print("playing");
                stimuli.Play();
                intpos = "" + EyeCenter.transform.position;
                introt = "(" + EyeCenter.transform.rotation.x + "," + EyeCenter.transform.rotation.y + "," + EyeCenter.transform.rotation.z + "," + EyeCenter.transform.rotation.w + ")";
                print("initail position is");
                print(intpos);
                print("initail rotation is");
                print(introt);
            }
            
            // play audio here 

        }
        if (t.gameObject.name == "Finish_button")
        {
            //SceneManager.LoadScene("Lobby", LoadSceneMode.Single);
        }
    }
		
	void Update () {
        if (trial_num < (stimuli_name.Length + stimuli_name_train.Length)){
            // trial condcut and record logic
            if (OVRInput.Get(OVRInput.Button.PrimaryIndexTrigger) == true && ispush == 0 && Play_button.activeSelf == false && Next_button.activeSelf == false){
                ispush = 1;
                Visualizer.GetComponent<Renderer>().material = Green;
                if (trial_num >= stimuli_name_train.Length) {
                        Debug.Log("Button One Pressed");
                        content = System.DateTime.Now + ";" + stimuli_name[trial_num - stimuli_name_train.Length].ToString() + ";" + intpos + ";" + introt + ";" + GSphere.transform.position + "\n";
                    }
            }
            //replay logic
            if (OVRInput.Get(OVRInput.Button.One) == true && ispush == 0 && ispush_2 == 0 && Play_button.activeSelf == false && Next_button.activeSelf == false)
            {
                ispush_2 = 1;
                if (trial_num < stimuli_name_train.Length)
                {
                    stimuli = GetComponent<AudioSource>();
                    stimuli.clip = Resources.Load<AudioClip>(stimuli_name_train[trial_num] + "_" + audio_id_name[audio_id] + "_" + set_id_name[set_id]);
                    stimuli.Play();
                    Debug.Log("Button One Pressed");
                }
                else
                {
                    stimuli = GetComponent<AudioSource>();
                    stimuli.clip = Resources.Load<AudioClip>(stimuli_name[trial_num - stimuli_name_train.Length] + "_" + audio_id_name[audio_id] + "_" + set_id_name[set_id]);
                    stimuli.Play();
                    intpos = "" + EyeCenter.transform.position;
                    introt = "(" + EyeCenter.transform.rotation.x + "," + EyeCenter.transform.rotation.y + "," + EyeCenter.transform.rotation.z + "," + EyeCenter.transform.rotation.w + ")";
                    Debug.Log("Button One Pressed");
                }
                
            }

            if (OVRInput.Get(OVRInput.Button.One) == false && ispush_2 == 1)
            {
                ispush_2 = 0;
            }
            //Finish trail logic
            if (OVRInput.Get(OVRInput.Button.PrimaryIndexTrigger) == false && ispush == 1){
                ispush = 0;
                Vector3 eye_center = EyeCenter.transform.position;
                Next_button.transform.position = new Vector3(Convert.ToSingle(20 * Math.Sin(Convert.ToDouble(EyeCenter.transform.eulerAngles.y) * Math.PI / 180)), Play_button.transform.position.y, Convert.ToSingle(20 * Math.Cos(Convert.ToDouble(EyeCenter.transform.eulerAngles.y) * Math.PI / 180)));
                Next_button.transform.eulerAngles = new Vector3(Next_button.transform.eulerAngles.x, EyeCenter.transform.eulerAngles.y, Next_button.transform.eulerAngles.z);
                Next_button.SetActive(true);
                Visualizer.GetComponent<Renderer>().material = Red;
            }
            if(OVRInput.Get(OVRInput.Button.Two) == true && Next_button.activeSelf == true){
                SceneManager.LoadScene(SceneManager.GetActiveScene().name);
                print(trial_num);
            }
        }
    }

}
