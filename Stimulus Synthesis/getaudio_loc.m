%% 
clear all
clc

fs = 44100;
dt = 1/fs;

azi = [-80, -35, 0, 45, 65];
azn = [1, 6, 13, 22, 24];
ele = [-22.5, 39.375, -16.875, 0, 73.125];
eln = [4, 15, 5, 8, 21];
music = audioread('anechoic_audio/Cello_new.wav');
%noise = audioread('anechoic_audio/Noise.wav');
speech = audioread('anechoic_audio/Speech.wav');
music = music(1:44100*5, 1);
noise = pinknoise(fs*3);
speech = speech(1:44100*4, 1);

audio_id = ["speech", "noise", "music"];
hrtf_id = ["generic", "est" ];

hrir_right = csvread('hrtf_est_location/sub0_est_right.csv');
hrir_left = csvread('hrtf_est_location/sub0_est_left.csv');

for i = 1:1:length(audio_id)
    if audio_id(i) == "speech"
        imp = speech;
    elseif audio_id(i) == "noise"
        imp = noise;
    else
        imp = music;
    end
    for j = 1:1:5
        azi_angle = azi(j);
        an = azn(j);
        el_angle =ele(j);
        filename = sprintf('%d_%s_%s.wav', j, audio_id(i), hrtf_id(1));
        filename_est = sprintf('%d_%s_%s.wav', j, audio_id(i), hrtf_id(2));
        index = (an-1)*50+eln(j)
        hrir_est(:,1) = hrir_left(index+1, :);
        hrir_est(:,2) = hrir_right(index+1, :);
        [hrir,azi_angle,el_angle] = get_hrir(azi_angle,el_angle,'Subject',21,'Plot','on'); %sub_id
        % HRIR_est = AnechoicBRIR(hrir_est, fs);
        % HRIR = AnechoicBRIR(hrir, fs);
        N = max(size(hrir));
        t = (0:N-1)*dt;t=t.';

        new_sound_1 = zeros(length(imp),2);
        new_sound_2 = zeros(length(imp),2);
        new_sound_1(:,1) = fftfilt(hrir(:,1),imp); %left channel
        new_sound_1(:,2) = fftfilt(hrir(:,2),imp); %right channel
        new_sound_2(:,1) = fftfilt(hrir_est(:,1),imp); %left channel
        new_sound_2(:,2) = fftfilt(hrir_est(:,2),imp); %right channel
        
        y = rms(vertcat(new_sound_1(:,1),new_sound_1(:,2)));
        y_est = rms(vertcat(new_sound_2(:,1),new_sound_2(:,2)));

        if y > y_est
            new_sound_1 = new_sound_1.*(y_est/y);
        else
            new_sound_2 = new_sound_2.*(y/y_est);
        end

        y = rms(vertcat(new_sound_1(:,1),new_sound_1(:,2)));
        y_est = rms(vertcat(new_sound_2(:,1),new_sound_2(:,2)));


        new_max = max(max(abs(new_sound_1)));
        new_max_est = max(max(abs(new_sound_2)));
        newmax = max(new_max, new_max_est);

        new_sound_1 = new_sound_1./newmax;
        new_sound_2 = new_sound_2./newmax;

        audiowrite(filename, new_sound_1, fs);  
        audiowrite(filename_est, new_sound_2, fs);
    end
end


%% get training t1-t4


clear all
clc

fs = 44100;
dt = 1/fs;

azi = [-45, -30, -5, 15];
azn = [4, 7, 12, 16];
ele = [-28.125, 22.5, -16.875, -5.625];
eln = [3, 12, 5, 7];
music = audioread('anechoic_audio/Cello_new.wav');
%noise = audioread('anechoic_audio/Noise.wav');
speech = audioread('anechoic_audio/Speech.wav');
music = music(1:44100*5, 1);
noise = pinknoise(fs*3);
speech = speech(1:44100*3, 1);

audio_id = ["speech", "noise", "music"];
hrtf_id = ["generic", "est" ];

hrir_right = csvread('hrtf_est_location/sub0_est_right.csv');
hrir_left = csvread('hrtf_est_location/sub0_est_left.csv');

for i = 1:1:length(audio_id)
    if audio_id(i) == "speech"
        imp = speech;
    elseif audio_id(i) == "noise"
        imp = noise;
    else
        imp = music;
    end
    for j = 1:1:4
        azi_angle = azi(j);
        an = azn(j);
        el_angle =ele(j);
        filename = sprintf('t%d_%s_%s.wav', j, audio_id(i), hrtf_id(1))
        filename_est = sprintf('t%d_%s_%s.wav', j, audio_id(i), hrtf_id(2))
        index = (an-1)*50+eln(j);
        hrir_est(:,1) = hrir_left(index+1, :);
        hrir_est(:,2) = hrir_right(index+1, :);
        [hrir,azi_angle,el_angle] = get_hrir(azi_angle,el_angle,'Subject',21,'Plot','on'); %sub_id
        N = max(size(hrir));
        t = (0:N-1)*dt;t=t.';

        new_sound_1 = zeros(length(imp),2);
        new_sound_2 = zeros(length(imp),2);
        new_sound_1(:,1) = fftfilt(hrir(:,1),imp); %left channel
        new_sound_1(:,2) = fftfilt(hrir(:,2),imp); %right channel
        new_sound_2(:,1) = fftfilt(hrir_est(:,1),imp); %left channel
        new_sound_2(:,2) = fftfilt(hrir_est(:,2),imp); %right channel

        y = rms(vertcat(new_sound_1(:,1),new_sound_1(:,2)))
        y_est = rms(vertcat(new_sound_2(:,1),new_sound_2(:,2)))

        if y > y_est
            new_sound_1 = new_sound_1.*(y_est/y);
        else
            new_sound_2 = new_sound_2.*(y/y_est);
        end

        y = rms(vertcat(new_sound_1(:,1),new_sound_1(:,2)))
        y_est = rms(vertcat(new_sound_2(:,1),new_sound_2(:,2)))


        new_max = max(max(abs(new_sound_1)))
        new_max_est = max(max(abs(new_sound_2)))
        newmax = max(new_max, new_max_est)

        new_sound_1 = new_sound_1./newmax;
        new_sound_2 = new_sound_2/newmax;

        %sound(new_sound, 44100);

        audiowrite(filename, new_sound_1, fs);  
        audiowrite(filename_est, new_sound_2, fs);
    end
end

%%
N = 176400;
t = (0:N-1).'/fs;

x1 = sin(2*pi*440*t);
x2 = zeros(N,1);

left = [x1,1/6*x1];
right = [1/6*x1,x1];
soundsc(left,fs);
pause;
soundsc(right,fs);
