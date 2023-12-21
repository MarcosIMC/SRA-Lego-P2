function [] = ShowPlayerStageLog(filename, th0)
% IN: 
%   filename - log filename [char]
%   th0 - initial robot angle [rad]
% OUT: 
%   nothing
% EXAMPLE:
%   ShowPlayerStageLog('mydata2018_02_26_14_42_05.log', 45/180*pi)

  [pos obs] = ExtractPathScans(filename,th0);
  
  precision=1e-9;
  
  hold on;
  axis equal;
  grid on;
  
  xlabel('x (m)');
  ylabel('y (m)');

  trajectory_init_color=[0 1 0]; % green
  trajectory_last_color=[1 0 0]; % red 

  % drawing trajectory points (odometry)
  for i=1:size(pos.x,2)
    lambda=i/size(pos.x,2);
    plot(pos.x(i),pos.y(i),'.','Color',trajectory_init_color*(1-lambda)+trajectory_last_color*lambda); 
  end

  sensory_init_color=[0 1 1]; % cyan 
  sensory_last_color=[0 0 0]; % black 

  % drawing sensor readings (laser)
  for i=1:size(obs.x,2)
    lambda=i/size(obs.x,2);
    plot(obs.x{i}(:),obs.y{i}(:),'.','Color',sensory_init_color*(1-lambda)+sensory_last_color*lambda);
  end

return;
