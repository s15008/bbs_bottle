% rebase('./template/base.tpl')
  <h1>唯一版</h1>
  <dl>
    % for res in reses:
      <dt>{{res.get('id')}} {{res.get('name')}} {{res.get('created_date')}}</dt>
      <dd>{{res.get('message')}}</dd>
    % end
  </dl>
