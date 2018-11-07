# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 20:05:33 2018

@author: houchw
"""

import scrapy

class ChinaClinicalSpider(scrapy.Spider):
    name = "clinicalSpider"
    allowed_domains = ['chinadrugtrials.org.cn']
    start_urls = ["http://www.chinadrugtrials.org.cn/eap/clinicaltrials.searchl\
                  istdetail?ckm_index={}&currentpage=1&pagesize=20&rule=CTR&sort=\
                  desc&sort2=desc".format(i) for i in range(1, 6864)]
    
    def parse(self, response):
        # 题目和背景信息
        ctr_number = reponse.xpath('//*[@id="div_open_close_01"]/table[1]/tbody/tr[1]/td[2]').extract() #登记号
        """
        conditions = scrapy.Field() #适应症
        public_title = scrapy.Field() #试验通俗题目
        scientific_title = scrapy.Field()  #试验专业题目
        plan_version = scrapy.Field() #试验方案编号
        accept_id = scrapy.Field() #临床申请受理号
        drug_name = scrapy.Field() #药物名称
        drug_type = scrapy.Field() #化学药物
        
        # 申办者信息
        sponsors = scrapy.Field() #申办者名称
        applicant = scrapy.Field() #联系人姓名
        applicant_telephone = scrapy.Field() #联系人电话
        applicant_Email = scrapy.Field() #联系人邮箱
        applicant_address = scrapy.Field() #联系人邮政地址
        applicant_postcode = scrapy.Field() #联系人邮编
        sources_of_funding = scrapy.Field() #试验项目经费来源
        
        # 临床试验信息
        purpose = scrapy.Field() # 试验目的
        
        ## 试验设计
        study_type = scrapy.Field() # 试验分类
        phase = scrapy.Field() # 试验分期
        intervention_model = scrapy.Field() #设计类型
        allocation = scrapy.Field() #随机化
        masking = scrapy.Field() #盲法
        study_domain = scrapy.Field() #试验范围
        
        ## 受试者信息
        age = scrapy.Field() #年龄
        gender = scrapy.Field() #性别
        accepts_healthy_volunteers = scrapy.Field() #健康受试者：有或无
        inclusion_criteria = scrapy.Field() #入选标准
        exclusion_criteria = scrapy.Field() #排除标准
        estimated_enrollment = scrapy.Field() #目标入组人数
        actual_enrollment = scrapy.Field() #实际入组人数
        
        ## 试验分组
        experimental_drug_name = scrapy.Field() #试验药名称
        experimental_drug_usage = scrapy.Field() #试验药用法
        placebo_drug_name = scrapy.Field() #对照药名称
        placebo_drug_usage = scrapy.Field() #对照药用法
        
        ## 终点指标
        primary_outcome_measures = scrapy.Field() #主要终点指标
        primary_outcome_measures_date = scrapy.Field() #评价时间
        primary_outcome_measures_choice = scrapy.Field() #终点指标选择
        secondary_outcome_measures = scrapy.Field() #次要终点指标
        secondary_outcome_measures_date = scrapy.Field() #评价时间
        secondary_outcome_measures_choice = scrapy.Field() #终点指标选择
        
        ## 数据安全监察委员会
        data_management_committee = scrapy.Field()
        
        ## 为受试者购买试验伤害保险
        insurance_for_subject = scrapy.Field()
        
        # 第一例受试者入组日期
        first_subject_included_date = scrapy.Field()
        
        # 试验终止日期
        study_ending_date = scrapy.Field()
        
        # 研究者信息
        
        ## 主要研究者信息
        study_leader_name = scrapy.Field()
        study_leader_title = scrapy.Field() #职称
        study_leader_phone = scrapy.Field()
        study_leader_email = scrpay.Field()
        study_leader_address = scrapy.Field()
        study_leader_postcode = scrapy.Field()
        study_leader_institution = scrapy.Field()
        
        ## 各参加机构信息
        study_site_name = scrapy.Field()
        study_site_pi = scrapy.Field()
        study_site_country = scrapy.Field()
        study_site_province = scrapy.Field()
        study_site_city = scrapy.Field()
        
        # 伦理委员会信息
        ethic_committee_name = scrapy.Field()
        ethic_committee_approved = scrapy.Field()
        ethic_committee_approved_date = scrapy.Field()
        
        # 试验状态
        recruitment_status = scrapy.Field()
        
        # 信息更新记录
        updated_date = scrapy.Field() #信息更新时间
        updated_recored = scrapy.Field() # 信息更新记录
        """