function [hrir,az,el] = get_hrir(az,el,varargin)

    if nargin < 3
        subj = '021';
    end
    if mod(length(varargin),2)>0
        error("Format: 'Option','OptionValue'");
    end
    
    plot_it = 0;
    for ii = (1:2:length(varargin))
        if ~isempty(strfind('Subject',varargin{ii}))
            if ischar(varargin{ii+1})
                subj = varargin{ii+1};
            else
                subj = num2str(varargin{ii+1});
            end
        elseif ~isempty(strfind('Plot',varargin{ii}))
            if ischar(varargin{ii+1})
                if ~isempty(strfind('on',varargin{ii+1}))
                    plot_it = 1;
                else
                    plot_it = 0;
                end
            else
                error('Expecting string...');
            end
        else
            error([varargin{ii}," is not an available option."]);
        end
    if length(subj)<3
        subj = ['0',subj];
    end
    
    subj_found = 0;
    cipic_dir = dir('CIPIC');
    cipic_dir = cipic_dir(3:end);
    for jj = 1:length(cipic_dir)
        if ~isempty(strfind(cipic_dir(jj).name,subj))
            load(['CIPIC\',cipic_dir(jj).name,'\hrir_final.mat']);
            subj_found = 1;
            break;
        end
    end
    if subj_found == 0
        error('Subject number does not exist.');
    end
    azs = [-80,-65,-55,-45:5:45,55,65,80];
    els = -45+5.625*(0:49);els=els.';

    fs = 44100;
    dt = 1/fs;
    [~,~,N] = size(hrir_l);
    t = (0:N-1)*dt;t=t.';

    if az>90
        az = az-180;
        el = 180-el;
    elseif az<-90
        az = az+180;
        el = 180-el;
    end

    [~,naz] = min(abs(azs-az));
    [~,nel] = min(abs(els-el));

    hrir_left = squeeze(hrir_l(naz,nel,:));
    hrir_right = squeeze(hrir_r(naz,nel,:));
    hrir = [hrir_left,hrir_right];
    az = azs(naz);
    el = els(nel);
    
    if plot_it == 1
        x = sin(azs*pi/180);
        y = cos(els*pi/180)*cos(azs*pi/180);
        z = sin(els*pi/180)*cos(azs*pi/180);
        front_x = sin(0);
        front_y = cos(0)*cos(0);
        front_z = sin(0)*cos(0);
        sp_x = sin(az*pi/180);
        sp_y = cos(el*pi/180)*cos(az*pi/180);
        sp_z = sin(el*pi/180)*cos(az*pi/180);

        figure(101)
        allPlot = plot3(x,y,z,'LineStyle','none','Color','k','Marker','o','MarkerFaceColor','k','MarkerSize',2);
        hold on;
        frontPlot = plot3(front_x,front_y,front_z,'LineStyle','none','Color','r','Marker','^','MarkerFaceColor','r','MarkerSize',10);
        spPlot = plot3(sp_x,sp_y,sp_z,'LineStyle','none','Color','b','Marker','o','MarkerFaceColor','b','MarkerSize',10);
        hold off;
        set(allPlot,'HandleVisibility','off');
        legend('Front','Speaker Location','Location','northwest');
        view([180-37.5,30]);
    end
end